from rest_framework import serializers
from .models import Dog


class DogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    characteristics = serializers.StringRelatedField(many=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Dog
        fields = ['id', 'owner', 'name', 'breed', 'birthday', 'size',
                  'gender', 'characteristics', 'is_adopted',
                  'created_at', 'updated_at']
