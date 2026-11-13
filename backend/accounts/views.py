from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import EditAccountSerializer, RegisterSerializer, UserSerializer


def token_for(user):
    return {'token': str(AccessToken.for_user(user))}


# POST /auth/register
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(token_for(user), status=status.HTTP_201_CREATED)


# POST /auth/login
@api_view(['POST'])
def login(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    if not User.objects.filter(username=username).exists():
        return Response('There is no user with that username.', status=status.HTTP_401_UNAUTHORIZED)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response('Incorrect password.', status=status.HTTP_401_UNAUTHORIZED)
    return Response(token_for(user))


# GET /auth/account
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    return Response(UserSerializer(request.user).data)


# PATCH /auth/account/<id>/edit  (always edits the logged-in user's own account)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_account(request, pk):
    serializer = EditAccountSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response('User successfully updated')


# GET /auth/users  (admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def users(request):
    return Response(UserSerializer(User.objects.all(), many=True).data)


# DELETE /auth/user/<id>  (admin only)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, pk):
    get_object_or_404(User, pk=pk).delete()
    return Response('User successfully deleted')


# PATCH /auth/admin/<id>  (admin only) body: {"isAdmin": true}
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def set_admin(request, pk):
    is_admin = request.data.get('isAdmin')
    if not isinstance(is_admin, bool):
        return Response({'isAdmin': 'Must be true or false.'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, pk=pk)
    user.is_staff = is_admin
    user.save(update_fields=['is_staff'])
    return Response(UserSerializer(user).data)
