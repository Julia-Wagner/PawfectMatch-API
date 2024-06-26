from django.db import IntegrityError
from rest_framework import serializers
from saves.models import Save


class SaveSerializer(serializers.ModelSerializer):
    """
    Serializer for the Save model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Save
        fields = ['id', 'created_at', 'owner', 'post']

    def create(self, validated_data):
        """
        Create a new dave instance and check for duplicates
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
