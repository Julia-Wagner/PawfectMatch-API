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
    address = serializers.SerializerMethodField()

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

    def get_address(self, obj):
        """
        Return the owner's phone number if available.
        """
        address_details = []
        if obj.address_1:
            address_details.append(obj.address_1)
        if obj.address_2:
            address_details.append(obj.address_2)
        if obj.city:
            address_details.append(f"{obj.city}")
        if obj.postcode:
            address_details.append(f"{obj.postcode}")
        if obj.country:
            address_details.append(f"{obj.country}")

        return ', '.join(
            address_details) if address_details else "No address available."

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'phone_number',
            'address_1', 'address_2', 'city', 'postcode', 'country',
            'description', 'type', 'image', 'is_owner', 'following_id',
            'posts_count', 'dogs_count', 'followers_count', 'following_count',
            'comments_count', 'address', 'mail_address'
        ]
