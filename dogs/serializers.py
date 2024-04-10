from rest_framework import serializers
from .models import Dog, DogCharacteristic


class DogCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogCharacteristic
        fields = ['id', 'characteristic']


class DogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    characteristics = serializers.PrimaryKeyRelatedField(
        queryset=DogCharacteristic.objects.all(),
        many=True,
        allow_null=True,
        required=False)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Dog
        fields = ['id', 'owner', 'is_owner', 'name', 'breed', 'birthday',
                  'size', 'gender', 'characteristics', 'is_adopted',
                  'created_at', 'updated_at']
