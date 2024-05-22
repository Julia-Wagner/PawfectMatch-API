from django_filters.rest_framework import (DjangoFilterBackend, FilterSet)
from django_filters import filters
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from pawfect_api.permissions import IsOwnerOrReadOnly, IsShelterOrReadOnly
from .models import Dog, DogCharacteristic
from .serializers import DogSerializer, DogCharacteristicSerializer


class DogFilter(FilterSet):
    """
    Custom filterset to allow filtering dogs based on characteristics.
    """
    characteristics = filters.ModelMultipleChoiceFilter(
        queryset=DogCharacteristic.objects.all(),
        field_name='characteristics__id',
        to_field_name='id',
        conjoined=True)

    class Meta:
        model = Dog
        fields = ['breed', 'size', 'gender', 'is_adopted', 'characteristics']


class DogList(generics.ListCreateAPIView):
    """
    List all dogs.
    Create a dog if logged in and user is shelter.
    perform_create: associate the dog with the logged-in user.
    """
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly
                          & IsShelterOrReadOnly]
    queryset = Dog.objects.all()
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = DogFilter
    search_fields = [
        'owner__username',
        'name',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a dog and edit or delete it if you own it.
    """
    serializer_class = DogSerializer
    permission_classes = [IsOwnerOrReadOnly & IsShelterOrReadOnly]
    queryset = Dog.objects.all()


class DogCharacteristicList(generics.ListAPIView):
    """
    List all dog characteristics.
    Create a new one if logged in and user is shelter.
    """
    serializer_class = DogCharacteristicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = DogCharacteristic.objects.all()


class DogCharacteristicDetail(generics.RetrieveAPIView):
    """
    Retrieve a dog characteristic and edit or delete it if you own it.
    """
    serializer_class = DogCharacteristicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = DogCharacteristic.objects.all()
