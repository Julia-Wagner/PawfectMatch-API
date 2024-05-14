from rest_framework import serializers

from followers.models import Follower
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    dogs_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the profile
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        Get the ID of the follow for the current user and the profile owner
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'phone_number',
            'address_1', 'address_2', 'city', 'postcode', 'country',
            'description', 'type', 'image', 'is_owner', 'following_id',
            'posts_count', 'dogs_count', 'followers_count', 'following_count',
            'comments_count'
        ]
