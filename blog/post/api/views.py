from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     UpdateAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,)
from rest_framework.mixins import CreateModelMixin

from rest_framework.permissions import (IsAuthenticated, IsAdminUser,)

from post.api.paginations import PostPagination
from post.api.permission import IsOwner
from post.api.serializers import (PostSerializers, PostModalSerializers, PostCreateUpdateModalSerializers,)
from post.models import Post


class PostListAPIView(ListAPIView, CreateModelMixin):
    # queryset = Post.objects.all()
    serializer_class = PostModalSerializers
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    # pagination
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        query = self.request.GET.get('q')
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModalSerializers
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModalSerializers
    lookup_field = 'slug'

    permission_classes = [IsOwner]


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateModalSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateModalSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
