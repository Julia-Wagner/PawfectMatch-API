from rest_framework import serializers
from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def validate(self, attrs):
        # get the type to validate
        media_type = attrs.get('type')

        if media_type == 'image':
            image = attrs.get('image')
            if image:
                if image.size > 2 * 1024 * 1024:
                    raise serializers.ValidationError(
                        'Image size larger than 2MB!')
                if image.image.height > 4096:
                    raise serializers.ValidationError(
                        'Image height larger than 4096px!'
                    )
                if image.image.width > 4096:
                    raise serializers.ValidationError(
                        'Image width larger than 4096px!'
                    )
        elif media_type == 'video':
            video = attrs.get('video')
            if video:
                if video.size > 50 * 1024 * 1024:
                    raise serializers.ValidationError(
                        'Video size larger than 50MB!')
                if not video.name.endswith('.mp4'):
                    raise serializers.ValidationError(
                        'Only MP4 video format allowed!')
            else:
                raise serializers.ValidationError('No video uploaded!')
        else:
            raise serializers.ValidationError('Invalid media type!')

        return attrs

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Media
        fields = [
            'id', 'owner', 'is_owner', 'image', 'video',
            'name', 'description', 'type', 'is_main_image',
            'created_at', 'updated_at'
        ]
