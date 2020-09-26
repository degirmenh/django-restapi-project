from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import Serializer, CharField, ModelSerializer, ImageField, DateTimeField, \
    ValidationError

from post.models import Post


class PostSerializers(Serializer):
    title = CharField(max_length=200)
    content = CharField(max_length=2000)
    image = ImageField()
    slug = CharField()
    created = DateTimeField()


class PostModalSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='post:detail', lookup_field='slug')
    username = SerializerMethodField(method_name='username_new')

    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            "content",
            "image",
            "url",
            "created",
            "modified_by",
            'username'
        ]

    @staticmethod
    def username_new(obj):
        return str(obj.user.username)


class PostCreateUpdateModalSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='post:detail', lookup_field='slug')

    class Meta:
        model = Post
        fields = [
            'title',
            "content",
            "image",
        ]

    """
        def update(self, instance, validate_data):
        instance.title = validate_data.get('title', instance.title)
        instance.content = validate_data.get('content', instance.content)
        instance.image = validate_data.get('image', instance.image)
        instance.save()
        return instance

    def create(self, validated_data):
        print(self.context['request'].user)
        print(validated_data)
        return Post.objects.create(**validated_data)

    @staticmethod
    def validate_title(value):
        if value == "hakan":
            raise ValidationError('Bu deger olmaz')
        return True

    def validate(self, attrs):
        print(attrs)
        return True

    
    """
