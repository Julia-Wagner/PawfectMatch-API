from django.db import models
from django.contrib.auth.models import User

from dogs.models import Dog


class Post(models.Model):
    """
    Post model.
    Images handled in separate medias app.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='posts')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dogs = models.ManyToManyField(Dog, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
