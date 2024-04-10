from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from pawfect_api.permissions import IsOwnerOrReadOnly, IsShelter
from .models import Dog
from .serializers import DogSerializer


class DogList(APIView):
    """
    List dogs or create a dog if logged in and user is shelter.
    """
    serializer_class = DogSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsShelter
    ]

    def get(self, request):
        dogs = Dog.objects.all()
        serializer = DogSerializer(
            dogs, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = DogSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class DogDetail(APIView):
    """
    Retrieve a dog and edit or delete it if you own it.
    """
    permission_classes = [
        IsOwnerOrReadOnly,
        IsShelter
    ]
    serializer_class = DogSerializer

    def get_object(self, pk):
        try:
            dog = Dog.objects.get(pk=pk)
            self.check_object_permissions(self.request, dog)
            return dog
        except Dog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dog = self.get_object(pk)
        serializer = DogSerializer(
            dog, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        dog = self.get_object(pk)
        serializer = DogSerializer(
            dog, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        dog = self.get_object(pk)
        dog.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
