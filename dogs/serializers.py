from django.utils import timezone
from rest_framework import serializers

from medias.serializers import MediaSerializer
from profiles.models import Profile
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
    owner_name = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    owner_address = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    characteristics = serializers.PrimaryKeyRelatedField(
        queryset=DogCharacteristic.objects.all(),
        many=True,
        allow_null=True,
        required=False)
    characteristics_names = DogCharacteristicSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()
    additional_images = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    birthday_formatted = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the dog
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_owner_name(self, obj):
        """
        Return the owner's name if available, otherwise return the username.
        """
        owner_profile = Profile.objects.get(owner=obj.owner)
        return owner_profile.name if hasattr(owner_profile, 'name') \
            else obj.owner.username

    def get_owner_phone(self, obj):
        """
        Return the owner's phone number if available.
        """
        owner_profile = Profile.objects.get(owner=obj.owner)
        return owner_profile.phone if hasattr(owner_profile, 'phone') \
            else "No phone number available"

    def get_owner_address(self, obj):
        """
        Return the owner's phone number if available.
        """
        owner_profile = Profile.objects.get(owner=obj.owner)
        address_details = []
        if owner_profile.address_1:
            address_details.append(owner_profile.address_1)
        if owner_profile.address_2:
            address_details.append(owner_profile.address_2)
        if owner_profile.city:
            address_details.append(f"{owner_profile.city}")
        if owner_profile.postcode:
            address_details.append(f"{owner_profile.postcode}")
        if owner_profile.country:
            address_details.append(f"{owner_profile.country}")

        return ', '.join(
            address_details) if address_details else "No address available."

    def get_profile_id(self, obj):
        """
        Return the owner's profile id.
        """
        owner_profile = Profile.objects.get(owner=obj.owner)
        return owner_profile.id

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

    def get_additional_images(self, obj):
        """
        Get the additional images associated with the dog
        """
        additional_media = obj.medias.filter(is_main_image=False, type='image')
        return MediaSerializer(additional_media,
                               many=True,
                               context=self.context).data

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

    def get_birthday_formatted(self, obj):
        """
        Return the birthday in dd.mm.yyyy format
        """
        return obj.birthday.strftime('%d.%m.%Y') if obj.birthday else None

    class Meta:
        model = Dog
        fields = ['id', 'owner', 'is_owner', 'owner_name', 'name', 'breed',
                  'birthday', 'birthday_formatted', 'size', 'gender',
                  'characteristics', 'is_adopted', 'age', 'description',
                  'main_image', 'created_at', 'updated_at', 'profile_id',
                  'owner_phone', 'owner_address', 'additional_images',
                  'characteristics_names']
