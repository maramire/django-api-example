from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


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
    get_followers = FollowerSerializer(many=True, read_only=True)
    get_following = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Profile
        fields = ['url', 'bio', 'is_private', 'pic', 'get_followers',
                  'get_following', 'posts']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        groups_data = validated_data.pop('groups')
        print(validated_data)
        user = User(**validated_data)
        user.save()

        for group in groups_data:
            user.groups.add(group)

        models.Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
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

        if (not instance.is_staff):
            profile = instance.profile
            profile_data = validated_data.pop('profile')
            profile.bio = profile_data.get('email', profile.bio)
            profile.is_private = profile_data.get(
                'is_private', profile.is_private)
            profile.pic = profile_data.get('pic', profile.pic)
            profile.save()

        return instance
