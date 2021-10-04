from django.contrib.auth.models import User, Group
from django.db.models.fields import CharField
from rest_framework import serializers
from . import models


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FollowerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Profile
        fields = ('url', 'pic', 'get_username')


class FollowingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Profile
        fields = ['url', 'pic', 'get_username']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        read_only=True, view_name="profile-posts")

    class Meta:
        model = models.Profile
        fields = ['url', 'bio', 'is_private', 'pic', 'get_followers_count',
                  'get_following_count', 'posts']


class ProfilePostSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = models.Profile
        fields = ['url', 'pic', 'username']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfilePostSerializer()

    class Meta:
        model = models.Comment
        fields = ['profile', 'text', 'date']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfilePostSerializer()
    # add the action resource as url
    comments = serializers.HyperlinkedIdentityField(
        read_only=True, view_name="post-comments")

    class Meta:
        model = models.Post
        fields = ['url', 'caption', 'date', 'image', 'profile', 'comments']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'profile']

    # Define the way how a user can be created with a profile object
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        groups_data = validated_data.pop('groups')
        user = User(**validated_data)
        user.save()
        for group in groups_data:
            user.groups.add(group)
        models.Profile.objects.create(user=user, **profile_data)
        return user

    # Define the way how the user can be updated with profile object
    def update(self, instance, validated_data):
        # update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()
        groups_data = validated_data.pop('groups')
        for group in groups_data:
            instance.groups.add(group)
        # update profile fields
        if (not instance.is_staff):
            profile = instance.profile  # the actual profile
            profile_data = validated_data.pop('profile')  # the updated profile
            profile.bio = profile_data.get('email', profile.bio)
            profile.is_private = profile_data.get(
                'is_private', profile.is_private)
            profile.pic = profile_data.get('pic', profile.pic)
            profile.save()

        return instance


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Post
