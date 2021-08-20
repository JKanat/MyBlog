
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view,action
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]
    # pagination_class = MyPaginationClass

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """переапрделим данныннй метод"""
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('week', 0))
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(weeks=weeks_count)
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


class CommentViewSet(PostViewSet, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
