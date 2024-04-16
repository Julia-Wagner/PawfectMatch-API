from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from pawfect_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    List posts.
    Create a post if logged in.
    perform_create: associate the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # user feed
        'owner__followed__owner__profile',
        # user saved posts
        'saves__owner__profile',
        # user posts
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'saves_count',
        'saves__created_at',
    ]

    def get_queryset(self):
        """
        Allow adding a query parameter to get dog posts.
        """
        queryset = Post.objects.annotate(
            saves_count=Count('saves', distinct=True),
            dog_count=Count('dogs', distinct=True)
        ).order_by('-created_at')

        if self.request.query_params.get('has_dogs') == 'true':
            queryset = queryset.filter(dog_count__gt=0)
        return queryset

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        saves_count=Count('saves', distinct=True)
    ).order_by('-created_at')
