
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view,action
from rest_framework import generics, status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .permissions import IsPostAuthor
from main.models import Category, Post, PostImage
# from main.serializers import CategorySerializer, PostSerializer, PostImageSerializer
from rest_framework import viewsets

from .serislizers import *

#
# class MyPaginationClass(PageNumberPagination):
#     page_size = 3
#
#     def get_paginated_response(self, data):
#         for i in range(self.page_size):
#             text = data[i]['text']
#             data[i]['text'] = text[:15] + '...'
#         return super().get_paginated_response(data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    # pagination_class = MyPaginationClass


    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """переапрделим данныннй метод"""
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(create_at__gte=start_date)
        return queryset

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(PostsViewSet, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer









class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """переапрделим данныннй метод"""
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permissions]



class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """переапрделим данныннй метод"""
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permissions]


class FavoritesViewSet(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    def get_permissions(self):
        """переапрделим данныннй метод"""
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permissions]



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

