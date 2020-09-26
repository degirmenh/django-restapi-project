from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from comment.models import Comment
from post.models import Post


class CommentSerializers(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created', ]

    def validate(self, attrs):
        if attrs['parent']:
            if attrs['parent'].post != attrs['post']:
                raise ValidationError('something went wrong!')
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id']


class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostCommentSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        # depth = 1

    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data


class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
