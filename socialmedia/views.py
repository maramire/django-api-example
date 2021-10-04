from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from socialmedia.serializers import UserSerializer, GroupSerializer, CommentSerializer, PostSerializer, ProfileSerializer
from . import models


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # manually define the queryset for the viewset
    # 'basename' on router is needed
    def get_queryset(self):
        if(self.request.user.is_staff):
            return models.Profile.objects.all()
        else:
            return models.Profile.objects.all().exclude(id=self.request.user.profile.id)


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if(user.is_staff):
            models.Post.objects.all()
        else:
            # make a queryset of only ids of people following
            following = user.profile.following.all().values_list('id', flat=True)
            # return the posts of people that user follows
            return models.Post.objects.filter(profile_id__in=following)
