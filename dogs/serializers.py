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

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the dog
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Dog
        fields = ['id', 'owner', 'is_owner', 'name', 'breed', 'birthday',
                  'size', 'gender', 'characteristics', 'is_adopted',
                  'created_at', 'updated_at']
