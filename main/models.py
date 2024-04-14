from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    profile_pic = models.ImageField(upload_to='media/profile/', blank=True, null=True)
    password = models.CharField(max_length=128)
    about = models.TextField(blank=True)
    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed_user')


class Post(models.Model):
    img = models.ImageField(upload_to='media/posts/img/', null=True, blank=True)
    video = models.FileField(upload_to='media/posts/video/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], blank=True)
    desc = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=50,default ="")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.TextField()

    def number_of_likes(self):
        return self.likes.count()
    