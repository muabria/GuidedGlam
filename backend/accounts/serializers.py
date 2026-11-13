from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from catalog.models import ColorSeason, FaceShape, SkinTone, SkinType, Undertone
from catalog.serializers import TagSerializer, UndertoneSerializer

from .models import User


# ---- Sending user info out ---------------------------------------------------

class BriefUserSerializer(serializers.ModelSerializer):
    """Just enough to show 'muabria (Tan, Dry, Heart)' next to a post or comment."""

    badgeShort = serializers.CharField(source='badge_short', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'badge', 'badgeShort']


class PublicUserSerializer(BriefUserSerializer):
    """A profile page as anyone can see it. No email."""

    skinTone = TagSerializer(source='skin_tone', read_only=True)
    skinType = TagSerializer(source='skin_type', read_only=True)
    faceShape = TagSerializer(source='face_shape', read_only=True)
    undertone = UndertoneSerializer(read_only=True)
    colorSeason = TagSerializer(source='color_season', read_only=True)
    followerCount = serializers.IntegerField(source='followers.count', read_only=True)
    followingCount = serializers.IntegerField(source='following.count', read_only=True)
    isFollowing = serializers.SerializerMethodField()

    class Meta(BriefUserSerializer.Meta):
        fields = BriefUserSerializer.Meta.fields + [
            'skinTone', 'skinType', 'faceShape', 'undertone', 'colorSeason',
            'followerCount', 'followingCount', 'isFollowing',
        ]

    def get_isFollowing(self, user):
        """Does the person looking at this profile follow them?"""
        request = self.context.get('request')
        viewer = getattr(request, 'user', None)
        if not viewer or not viewer.is_authenticated:
            return False
        return viewer.following.filter(pk=user.pk).exists()


class UserSerializer(PublicUserSerializer):
    """Your own account (or an admin's view): adds the private bits."""

    isAdmin = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta(PublicUserSerializer.Meta):
        fields = PublicUserSerializer.Meta.fields + ['email', 'isAdmin']


# ---- Taking user info in -----------------------------------------------------
# Each answer is sent as the id of the chosen option, e.g. {"skinTone": 7}.

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    # The three required sign-up questions.
    skinTone = PrimaryKeyRelatedField(source='skin_tone', queryset=SkinTone.objects.all())
    skinType = PrimaryKeyRelatedField(source='skin_type', queryset=SkinType.objects.all())
    faceShape = PrimaryKeyRelatedField(source='face_shape', queryset=FaceShape.objects.all())

    # Optional; can be filled in later from the profile page.
    undertone = PrimaryKeyRelatedField(queryset=Undertone.objects.all(), required=False, allow_null=True)
    colorSeason = PrimaryKeyRelatedField(source='color_season', queryset=ColorSeason.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'skinTone', 'skinType', 'faceShape', 'undertone', 'colorSeason']

    def create(self, validated_data):
        # create_user hashes the password for us.
        return User.objects.create_user(**validated_data)


class EditAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    skinTone = PrimaryKeyRelatedField(source='skin_tone', queryset=SkinTone.objects.all(), required=False)
    skinType = PrimaryKeyRelatedField(source='skin_type', queryset=SkinType.objects.all(), required=False)
    faceShape = PrimaryKeyRelatedField(source='face_shape', queryset=FaceShape.objects.all(), required=False)
    undertone = PrimaryKeyRelatedField(queryset=Undertone.objects.all(), required=False, allow_null=True)
    colorSeason = PrimaryKeyRelatedField(source='color_season', queryset=ColorSeason.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'skinTone', 'skinType', 'faceShape', 'undertone', 'colorSeason']
        extra_kwargs = {'username': {'required': False}, 'email': {'required': False}}

    def update(self, user, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(user, field, value)
        if password:
            user.set_password(password)
        user.save()
        return user
