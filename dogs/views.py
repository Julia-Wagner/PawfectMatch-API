from rest_framework import generics, permissions

from pawfect_api.permissions import IsOwnerOrReadOnly, IsShelterOrReadOnly
from .models import Dog, DogCharacteristic
from .serializers import DogSerializer, DogCharacteristicSerializer


class DogList(generics.ListCreateAPIView):
    """
    List all dogs.
    Create a dog if logged in and user is shelter.
    perform_create: associate the dog with the logged in user.
    """
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsShelterOrReadOnly]
    queryset = Dog.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a dog and edit or delete it if you own it.
    """
    serializer_class = DogSerializer
    permission_classes = [IsOwnerOrReadOnly & IsShelterOrReadOnly]
    queryset = Dog.objects.all()


class DogCharacteristicList(generics.ListCreateAPIView):
    """
    List all dog characteristics.
    Create a new one if logged in and user is shelter.
    """
    serializer_class = DogCharacteristicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsShelterOrReadOnly]
    queryset = DogCharacteristic.objects.all()


class DogCharacteristicDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a dog characteristic and edit or delete it if you own it.
    """
    serializer_class = DogCharacteristicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsShelterOrReadOnly]
    queryset = DogCharacteristic.objects.all()
