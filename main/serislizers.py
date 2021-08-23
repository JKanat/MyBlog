from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'create_at', 'text')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = PostImageSerializer(instance.images.all(), many=True,
                                                       context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True,
                                                       context=self.context).data
        # representation['category'] = CategorySerializer(instance.category).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        return post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                url = ''
            return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author_email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment




class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = ('id', 'author', 'post', 'grade')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Rating.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Данный пользователь уже рейтнул этот пост.')

        rating = Rating.objects.create(
            **validated_data
        )

        return rating



class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = ('id', 'post', 'author', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data


        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Like.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Данный пользователь уже лайкнул этот пост.')

        like = Like.objects.create(
            **validated_data
        )

        return like


class FavoritesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'post', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Favorites.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Данный пост уже добавлен в избранное.')

        favorites = Favorites.objects.create(
            **validated_data
        )

        return favorites
