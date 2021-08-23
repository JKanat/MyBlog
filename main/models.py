from django.db import models


from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(MyUser,
                               on_delete=models.CASCADE,
                               related_name='comments')
    reply = models.ForeignKey(Post,
                              on_delete=models.CASCADE,
                              related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created', )


class Rating(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    grade = models.PositiveIntegerField()

    def __str__(self):
        return self.post.title


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title


class Favorites(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    name = models.CharField(max_length=50, default='Избранное')

    def __str__(self):
        return self.post.title