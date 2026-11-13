from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from catalog.views import id_param

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Anyone can look; only the person who made a post can change or delete it."""

    def has_object_permission(self, request, view, post):
        return request.method in permissions.SAFE_METHODS or post.author == request.user


# URL filter name -> the author's profile field,
# e.g. /api/post?skinType=1 shows posts by people with that skin type.
AUTHOR_FILTERS = {
    'skinTone': 'author__skin_tone',
    'skinType': 'author__skin_type',
    'faceShape': 'author__face_shape',
    'undertone': 'author__undertone',
    'colorSeason': 'author__color_season',
}


class PostViewSet(viewsets.ModelViewSet):
    """
    GET    /api/post            the feed (see filters in get_queryset)
    POST   /api/post            new post: caption, images (1-10 files), productIds
    GET    /api/post/<id>
    PATCH  /api/post/<id>       edit caption / products (author only)
    DELETE /api/post/<id>       (author only)
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        posts = Post.objects.select_related(
            'author__skin_tone', 'author__skin_type', 'author__face_shape',
        ).prefetch_related('images', 'products')
        params = self.request.query_params
        viewer = self.request.user

        for param, field in AUTHOR_FILTERS.items():
            if (pk := id_param(params, param)) is not None:
                posts = posts.filter(**{field: pk})
        if author := params.get('author'):                      # ?author=muabria
            posts = posts.filter(author__username=author)
        if (pk := id_param(params, 'product')) is not None:     # posts using a product
            posts = posts.filter(products=pk)
        if (pk := id_param(params, 'category')) is not None:    # posts using e.g. a blush
            posts = posts.filter(products__categories=pk)
        if search := params.get('search'):                      # words in the caption
            posts = posts.filter(caption__icontains=search)

        # These two only make sense when logged in.
        if params.get('following') == 'true':
            posts = posts.filter(author__in=viewer.following.all()) if viewer.is_authenticated else posts.none()
        if params.get('saved') == 'true':
            posts = posts.filter(saves=viewer) if viewer.is_authenticated else posts.none()

        return posts.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _toggle(self, request, relation):
        """Shared by like and save: POST adds you, DELETE removes you."""
        post = self.get_object()
        if request.method == 'POST':
            getattr(post, relation).add(request.user)
        else:
            getattr(post, relation).remove(request.user)
        return Response(self.get_serializer(post).data)

    # POST / DELETE /api/post/<id>/like
    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        return self._toggle(request, 'likes')

    # POST / DELETE /api/post/<id>/save
    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def save(self, request, pk=None):
        return self._toggle(request, 'saves')

    # GET / POST /api/post/<id>/comments
    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.select_related('user__skin_tone', 'user__skin_type', 'user__face_shape')
            return Response(CommentSerializer(comments, many=True).data)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# DELETE /api/comment/<id>  (the comment's writer, or the post's author)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user not in (comment.user, comment.post.author):
        return Response("You can't delete someone else's comment.", status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
