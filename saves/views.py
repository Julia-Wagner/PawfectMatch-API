from rest_framework import generics, permissions
from pawfect_api.permissions import IsOwnerOrReadOnly
from saves.models import Save
from saves.serializers import SaveSerializer


class SaveList(generics.ListCreateAPIView):
    """
    List saves.
    Create a save if logged in.
    perform_create: associate the save with the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaveSerializer

    def get_queryset(self):
        """
        Get the queryset for listing saves
        """
        user = self.request.user
        return Save.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Create a save and associate it with the logged-in user
        """
        serializer.save(owner=self.request.user)


class SaveDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a save or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SaveSerializer
    queryset = Save.objects.all()
