from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, ColorSeason, FaceShape, MakeupProduct, SkinTone, SkinType, Undertone
from .serializers import (
    CategorySerializer, ColorSeasonSerializer, FaceShapeSerializer, ProductSerializer,
    SkinToneSerializer, SkinTypeSerializer, UndertoneSerializer,
)


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


# The ones below are read-only here; add and edit them in the admin panel.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UndertoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Undertone.objects.all()
    serializer_class = UndertoneSerializer


class ColorSeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """Each season comes with its palette: the color guide."""

    queryset = ColorSeason.objects.prefetch_related('palette')
    serializer_class = ColorSeasonSerializer


# URL filter name -> model field, e.g. /api/product?category=2&skinType=1
PRODUCT_FILTERS = {
    'category': 'categories',
    'skinTone': 'skin_tones',
    'skinType': 'skin_types',
    'faceShape': 'face_shapes',
    'undertone': 'undertones',
    'colorSeason': 'color_seasons',
}


def id_param(params, name):
    """Read ?name=<number> from the URL; ignore it if it isn't a number."""
    value = params.get(name, '')
    return int(value) if value.isdigit() else None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = MakeupProduct.objects.prefetch_related(*PRODUCT_FILTERS.values())
        params = self.request.query_params
        for param, field in PRODUCT_FILTERS.items():
            if (pk := id_param(params, param)) is not None:
                products = products.filter(**{field: pk})
        if search := params.get('search'):
            products = products.filter(name__icontains=search)
        return products.distinct()
