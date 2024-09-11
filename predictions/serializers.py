from rest_framework import serializers
from .models import ImageUpload

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['image', 'user']

class ImageRepredectSerilzer(serializers.Serializer):
    id = serializers.IntegerField()

class SeachUserSerilizer(serializers.Serializer):
    user = serializers.CharField()
