from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'get_full_name', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['profile', 'text', 'date']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='profile-detail')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ['caption', 'date', 'image', 'profile', 'comments']


class FollowerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Profile
        fields = ('url', 'pic', 'get_username')


class FollowingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Profile
        fields = ['url', 'pic', 'get_username']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    get_followers = FollowerSerializer(many=True, read_only=True)
    get_following = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Profile
        fields = ['url', 'user', 'bio', 'is_private', 'pic', 'get_followers',
                  'get_following', 'posts']
