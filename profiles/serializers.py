from rest_framework import serializers
from .models import Profile
from django_countries.serializers import CountryFieldMixin


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'address_1', 'address_2', 'city', 'postcode',
            'country', 'description', 'type', 'image', 'is_owner'
        ]
