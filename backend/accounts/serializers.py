from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """What we send back about a user. The password is never included."""

    isAdmin = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isAdmin']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # create_user hashes the password for us.
        return User.objects.create_user(**validated_data)


class EditAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'username': {'required': False}, 'email': {'required': False}}

    def update(self, user, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(user, field, value)
        if password:
            user.set_password(password)
        user.save()
        return user
