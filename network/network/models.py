from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posters")
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now)
    likers = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"
    
    def serialize(self):
        return {
            "id": self.id,
            "body":self.body,
        }


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Follower")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")

