from rest_framework import serializers

from .models import FaceShape, SkinTone, SkinType


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
