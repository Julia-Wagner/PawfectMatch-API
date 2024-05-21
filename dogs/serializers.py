from django.utils import timezone
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
    characteristics = DogCharacteristicSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    birthday = serializers.SerializerMethodField()

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

    def get_age(self, obj):
        """
        Calculate the age of the dog based on its birthday
        https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
        """
        today = timezone.now().date()
        birth_date = obj.birthday
        age_in_years = (today.year - birth_date.year -
                        ((today.month, today.day)
                         < (birth_date.month, birth_date.day)))

        # Calculate the total days passed since the dog's birthday
        total_days_passed = (today.year * 365 + today.month * 30 + today.day -
                             birth_date.year * 365 - birth_date.month * 30 -
                             birth_date.day)

        # Convert days to months and weeks
        months_passed = total_days_passed // 30
        weeks_passed = total_days_passed // 7

        # Determine the age description
        if age_in_years >= 1:
            return f"{age_in_years} years old"
        elif months_passed >= 1:
            return f"{months_passed} months old"
        elif weeks_passed >= 1:
            return f"{weeks_passed} weeks old"
        else:
            return "Just born"

    def get_birthday(self, obj):
        """
        Return the birthday in dd.mm.yyyy format
        """
        return obj.birthday.strftime('%d.%m.%Y') if obj.birthday else None

    class Meta:
        model = Dog
        fields = ['id', 'owner', 'is_owner', 'name', 'breed', 'birthday',
                  'size', 'gender', 'characteristics', 'is_adopted', 'age',
                  'description', 'main_image', 'created_at', 'updated_at']
