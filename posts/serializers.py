from rest_framework import serializers

from dogs.models import Dog
from followers.models import Follower
from .models import Post
from saves.models import Save


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    dogs = serializers.PrimaryKeyRelatedField(
        queryset=Dog.objects.all(), many=True, required=False)
    save_id = serializers.SerializerMethodField()
    saves_count = serializers.ReadOnlyField()
    main_image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the post
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_is_following(self, obj):
        """
        Check if the current user is following the owner of the post
        """
        request = self.context['request']
        owner = obj.owner
        user = request.user
        if user.is_authenticated:
            following = Follower.objects.filter(owner=user,
                                                followed=owner).exists()
            return following
        return False

    def get_save_id(self, obj):
        """
        Get the ID of the save associated with the post for the current user
        """
        user = self.context['request'].user
        if user.is_authenticated:
            save = Save.objects.filter(
                owner=user, post=obj
            ).first()
            return save.id if save else None
        return None

    def get_main_image(self, obj):
        """
        Get the URL and the id of the main image associated with the post
        If no main image is found, a default image URL is returned
        """
        main_media = obj.medias.filter(is_main_image=True).first()
        if main_media:
            return {
                'id': main_media.id,
                'url': main_media.image.url
            }
        else:
            first_image_media = obj.medias.filter(type='image').first()
            if first_image_media:
                return {
                    'id': first_image_media.id,
                    'url': first_image_media.image.url
                }
        return {
            'id': None,
            'url':
                'https://res.cloudinary.com/drgviypka/image/upload/v1/no_image'
        }

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'title', 'type', 'content', 'created_at', 'updated_at', 'dogs',
            'save_id', 'saves_count', 'main_image', 'is_following'
        ]
