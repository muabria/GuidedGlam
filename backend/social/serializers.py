from rest_framework import serializers

from accounts.serializers import BriefUserSerializer
from catalog.models import MakeupProduct
from catalog.serializers import TagSerializer

from .models import Comment, Post, PostImage


class CommentSerializer(serializers.ModelSerializer):
    user = BriefUserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'createdAt']


class PostSerializer(serializers.ModelSerializer):
    author = BriefUserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    products = TagSerializer(many=True, read_only=True)
    likeCount = serializers.IntegerField(source='likes.count', read_only=True)
    commentCount = serializers.IntegerField(source='comments.count', read_only=True)
    liked = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    # Sent in when creating a post:
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, min_length=1, max_length=10,
    )
    productIds = serializers.PrimaryKeyRelatedField(
        source='products', queryset=MakeupProduct.objects.all(), many=True, write_only=True, required=False,
    )

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'caption', 'createdAt', 'products',
            'likeCount', 'commentCount', 'liked', 'saved', 'images', 'productIds',
        ]

    def _viewer(self):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return user if user and user.is_authenticated else None

    def get_liked(self, post):
        viewer = self._viewer()
        return bool(viewer) and post.likes.filter(pk=viewer.pk).exists()

    def get_saved(self, post):
        viewer = self._viewer()
        return bool(viewer) and post.saves.filter(pk=viewer.pk).exists()

    def to_representation(self, post):
        data = super().to_representation(post)
        # Photo addresses, e.g. "/media/posts/2026/11/look.jpg"
        data['images'] = [photo.image.url for photo in post.images.all()]
        return data

    def create(self, validated_data):
        images = validated_data.pop('images')
        products = validated_data.pop('products', [])
        post = Post.objects.create(**validated_data)
        post.products.set(products)
        for image in images:
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, post, validated_data):
        # Photos can't be swapped after posting; caption and products can.
        validated_data.pop('images', None)
        products = validated_data.pop('products', None)
        post.caption = validated_data.get('caption', post.caption)
        post.save()
        if products is not None:
            post.products.set(products)
        return post
