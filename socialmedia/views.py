from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from socialmedia.serializers import UserSerializer, GroupSerializer, CommentSerializer, PostSerializer, ProfileSerializer
from . import models


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
