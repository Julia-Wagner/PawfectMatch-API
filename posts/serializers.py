from rest_framework import serializers

from dogs.models import Dog
from .models import Post
from saves.models import Save


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    dogs = serializers.PrimaryKeyRelatedField(
        queryset=Dog.objects.all(), many=True, required=False)
    save_id = serializers.SerializerMethodField()
    saves_count = serializers.ReadOnlyField()
    main_image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_save_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            save = Save.objects.filter(
                owner=user, post=obj
            ).first()
            return save.id if save else None
        return None

    def get_main_image(self, obj):
        main_media = obj.medias.filter(is_main_image=True).first()
        if main_media:
            return main_media.image.url
        else:
            first_image_media = obj.medias.filter(type='image').first()
            if first_image_media:
                return first_image_media.image.url
        return ('https://res.cloudinary.com/drgviypka/image/upload/'
                'v1/f3hx6euwqexhgg3ehdik')

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'title', 'type', 'content', 'created_at', 'updated_at', 'dogs',
            'save_id', 'saves_count', 'main_image'
        ]
