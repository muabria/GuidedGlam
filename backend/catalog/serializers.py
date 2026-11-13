from rest_framework import serializers

from .models import (
    Category, ColorSeason, FaceShape, MakeupProduct, PaletteColor, SkinTone, SkinType, Undertone,
)


class TagSerializer(serializers.Serializer):
    """Read-only {id, name}, for showing any tag inside something else."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class FaceShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceShape
        fields = ['id', 'name']


class SkinToneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinTone
        fields = ['id', 'name']


class SkinTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinType
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class UndertoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Undertone
        fields = ['id', 'name', 'jewelry']


class PaletteColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletteColor
        fields = ['use', 'name', 'hex']


class ColorSeasonSerializer(serializers.ModelSerializer):
    palette = PaletteColorSerializer(many=True, read_only=True)

    class Meta:
        model = ColorSeason
        fields = ['id', 'name', 'palette']


class ProductSerializer(serializers.ModelSerializer):
    categories = TagSerializer(many=True, read_only=True)
    skinTones = TagSerializer(source='skin_tones', many=True, read_only=True)
    skinTypes = TagSerializer(source='skin_types', many=True, read_only=True)
    faceShapes = TagSerializer(source='face_shapes', many=True, read_only=True)
    undertones = TagSerializer(many=True, read_only=True)
    colorSeasons = TagSerializer(source='color_seasons', many=True, read_only=True)

    class Meta:
        model = MakeupProduct
        fields = [
            'id', 'name', 'description', 'price', 'categories',
            'skinTones', 'skinTypes', 'faceShapes', 'undertones', 'colorSeasons',
        ]
