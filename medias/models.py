from django.db import models
from django.contrib.auth.models import User

from cloudinary_storage.storage import VideoMediaCloudinaryStorage


class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='medias')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,
                             related_name='media')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=MEDIA_TYPES,
                            default='image')
    image = models.ImageField(
        upload_to='post_images/', default='../f3hx6euwqexhgg3ehdik',
        blank=True)
    video = models.FileField(upload_to='post_videos/',
                             blank=True, null=True,
                             storage=VideoMediaCloudinaryStorage())
    is_main_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Media for post {self.post.id}"
