from django.db import models
from django.db.models.fields import BooleanField, CharField, DateTimeField
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=140, blank=True)
    is_private = models.BooleanField(default=False)
    pic = models.ImageField(upload_to="images/profiles/", null=True)
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name="followers", blank=True)

    def __str__(self) -> str:
        return self.user.username

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def get_username(self):
        return self.user.username


class Post(models.Model):
    caption = models.CharField(max_length=140, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/posts/", null=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts")


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=140, blank=True)
    date = models.DateField(auto_now_add=True)
