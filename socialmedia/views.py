from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from socialmedia.serializers import FollowerSerializer, ProfilePostSerializer, UserSerializer, GroupSerializer, CommentSerializer, PostSerializer, ProfileSerializer
from . import models
from rest_framework.decorators import action
from rest_framework.response import Response


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
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # an action when posts/:id/comments is requested
    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        comments = models.Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


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

    # an action when profile/:id/posts is requested
    @action(methods=['get'], detail=True)
    def posts(self, request, pk=None):
        profile = get_object_or_404(models.Profile, pk=pk)
        # show posts if profiles is followed or is not private
        if (request.user.profile in profile.get_followers()) or not profile.is_private:
            posts = models.Post.objects.filter(profile_id=pk)
            serializer = PostSerializer(
                posts, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"message": f"You can't see {profile.user.username} posts because is a private account and you don't follow it."}, status=401)

    # an action when profile/:id/followers is requested
    @action(methods=['get'], detail=True)
    def followers(self, request, pk=None):
        profile = get_object_or_404(models.Profile, pk=pk)
        serializer = FollowerSerializer(
            profile.get_followers(), many=True, context={'request': request})
        return Response(serializer.data)

    # an action when profile/:id/following is requested
    @action(methods=['get'], detail=True)
    def following(self, request, pk=None):
        profile = get_object_or_404(models.Profile, pk=pk)
        serializer = FollowerSerializer(
            profile.get_following(), many=True, context={'request': request})
        return Response(serializer.data)

    # an action when profile/:id/follow is requested
    # 'request.user' is the user who follows
    # 'pk' is the id of the user that is followed
    @action(methods=['get'], detail=True)
    def follow(self, request, pk=None):
        my_following = request.user.profile.get_following()
        # check if user is already followed
        if my_following.filter(id__exact=int(pk)).exists():
            return Response({"message": "The profile is already being followed."})
        else:
            my_profile = request.user.profile
            following_profile = models.Profile.objects.get(id=int(pk))
            my_profile.following.add(following_profile)
            return Response({"message": f'Now you are following {following_profile.user.username}'})

    # an action when profile/:id/unfollow is requested
    # 'request.user' is the user who unfollows
    # 'pk' is the id of the user to unfollow
    @action(methods=['get'], detail=True)
    def unfollow(self, request, pk=None):
        my_following = request.user.profile.get_following()
        # check if user is already followed
        if my_following.filter(id__exact=int(pk)).exists():
            my_profile = request.user.profile
            following_profile = models.Profile.objects.get(id=int(pk))
            my_profile.following.remove(following_profile)
            return Response({"message": f"The profile {following_profile.user.username} has been unfollowed"})
        else:
            return Response({"message": "This profile can't be unfollowed because you're not following it"})


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
