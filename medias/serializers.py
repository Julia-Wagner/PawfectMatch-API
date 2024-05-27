from rest_framework import serializers
from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Media model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def validate_image(self, image):
        """
        Validate the uploaded image
        """
        if image.size > 8 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 8MB!')
        return image

    def validate_video(self, video):
        """
        Validate the uploaded video
        """
        if video.size > 50 * 1024 * 1024:
            raise serializers.ValidationError('Video size larger than 50MB!')
        if not video.name.endswith('.mp4'):
            raise serializers.ValidationError('Only MP4 video format allowed!')
        return video

    def validate(self, attrs):
        """
        Additional validation for the media type
        """
        media_type = attrs.get('type')

        if media_type == 'image':
            image = attrs.get('image')
            if not image:
                raise serializers.ValidationError('No image uploaded!')
            self.validate_image(image)
        elif media_type == 'video':
            video = attrs.get('video')
            if not video:
                raise serializers.ValidationError('No video uploaded!')
            self.validate_video(video)
        else:
            raise serializers.ValidationError('Invalid media type!')

        return attrs

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the media
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Media
        fields = [
            'id', 'owner', 'is_owner', 'image', 'video',
            'name', 'description', 'type', 'is_main_image',
            'created_at', 'updated_at'
        ]
