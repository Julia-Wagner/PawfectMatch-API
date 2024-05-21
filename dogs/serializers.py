from rest_framework import serializers
from .models import Dog, DogCharacteristic


class DogCharacteristicSerializer(serializers.ModelSerializer):
    """
    Serializer for the DogCharacteristic model
    """
    class Meta:
        model = DogCharacteristic
        fields = ['id', 'characteristic']


class DogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dog model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    characteristics = serializers.PrimaryKeyRelatedField(
        queryset=DogCharacteristic.objects.all(),
        many=True,
        allow_null=True,
        required=False)
    main_image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the dog
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_main_image(self, obj):
        """
        Get the URL and the id of the main image associated with the dog
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
        model = Dog
        fields = ['id', 'owner', 'is_owner', 'name', 'breed', 'birthday',
                  'size', 'gender', 'characteristics', 'is_adopted',
                  'description', 'main_image', 'created_at', 'updated_at']
