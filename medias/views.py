from rest_framework import generics, permissions, status
from rest_framework.response import Response

from dogs.models import Dog
from pawfect_api.permissions import IsOwnerOrReadOnly
from posts.models import Post
from .models import Media
from .serializers import MediaSerializer


class PostMediaList(generics.ListCreateAPIView):
    """
    List medias for post or create a media if logged in.
    """
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Media.objects.filter(post__pk=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = generics.get_object_or_404(Post, pk=post_id)
        serializer.save(owner=self.request.user, post=post)


class DogMediaList(generics.ListCreateAPIView):
    """
    List medias for dog or create a media if logged in.
    """
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        dog_id = self.kwargs['dog_id']
        return Media.objects.filter(dog__pk=dog_id)

    def perform_create(self, serializer):
        dog_id = self.kwargs.get('dog_id')
        dog = generics.get_object_or_404(Dog, pk=dog_id)
        serializer.save(owner=self.request.user, dog=dog)


class MediaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a media and edit or delete it if you own it.
    """
    serializer_class = MediaSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Media.objects.all()
