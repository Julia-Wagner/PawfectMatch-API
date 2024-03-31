from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from pawfect_api.permissions import IsOwnerOrReadOnly
from posts.models import Post
from .models import Media
from .serializers import MediaSerializer


class MediaList(APIView):
    """
    List medias for post or create a media if logged in.
    """
    serializer_class = MediaSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        medias = Media.objects.filter(post=post)
        serializer = MediaSerializer(
            medias, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = MediaSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.validated_data['post'] = post
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class MediaDetail(APIView):
    """
    Retrieve a media and edit or delete it if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = MediaSerializer

    def get_object(self, pk):
        try:
            media = Media.objects.get(pk=pk)
            self.check_object_permissions(self.request, media)
            return media
        except Media.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        media = self.get_object(pk)
        serializer = MediaSerializer(
            media, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        media = self.get_object(pk)
        serializer = MediaSerializer(
            media, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        media = self.get_object(pk)
        media.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
