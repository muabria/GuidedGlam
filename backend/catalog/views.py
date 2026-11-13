from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FaceShape, SkinTone, SkinType
from .serializers import FaceShapeSerializer, SkinToneSerializer, SkinTypeSerializer


@api_view(['GET'])
def test(request):
    return Response({'message': 'API is working!'})


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """GET (list + single), POST, PUT and PATCH. This one class replaces the
    five near-identical route handlers each table had in server/api/index.js."""


class FaceShapeViewSet(TagViewSet):
    queryset = FaceShape.objects.all()
    serializer_class = FaceShapeSerializer


class SkinToneViewSet(TagViewSet):
    queryset = SkinTone.objects.all()
    serializer_class = SkinToneSerializer


class SkinTypeViewSet(mixins.DestroyModelMixin, TagViewSet):
    """Skin types can also be deleted, but only when logged in."""

    queryset = SkinType.objects.all()
    serializer_class = SkinTypeSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
