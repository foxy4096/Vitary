from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


from django.contrib.auth.models import User

from apps.vit.serializers import VitSerializer
from . import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    paginator = PageNumberPagination()
    paginator.page_size = 100
    users = User.objects.all()
    users = paginator.paginate_queryset(users, request)
    serializer = serializers.UserSerializer(users, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    user = get_object_or_404(User, username=username)
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_vits(request, username):
    user = get_object_or_404(User, username=username)
    paginator = PageNumberPagination()
    paginator.page_size = 100
    vits = user.vit_set.all()
    vits = paginator.paginate_queryset(vits, request)
    serializer = VitSerializer(vits, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_followers(request, username):
    user = get_object_or_404(User, username=username)
    paginator = PageNumberPagination()
    paginator.page_size = 100
    followers = user.profile.followed_by.all()
    followers = paginator.paginate_queryset(followers, request)
    serializer = serializers.UserSerializer(followers, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_following(request, username):
    user = get_object_or_404(User, username=username)
    paginator = PageNumberPagination()
    paginator.page_size = 100
    following = user.profile.following.all()
    following = paginator.paginate_queryset(following, request)
    serializer = serializers.UserSerializer(following, many=True)
    return paginator.get_paginated_response(serializer.data)

