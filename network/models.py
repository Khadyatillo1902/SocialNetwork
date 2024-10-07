from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d-%b-%Y %H:%M:%S')}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_being_followed')

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
    
    class Meta:
        unique_together = ['user', 'user_follower']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.post}"