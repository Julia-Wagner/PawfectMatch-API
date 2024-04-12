from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content


class BannedWord(models.Model):
    """
    Banned word model, used to ensure appropriate comments
    """
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.word
