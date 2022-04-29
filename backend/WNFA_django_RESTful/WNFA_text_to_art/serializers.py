from dataclasses import field
from rest_framework import serializers
from .models import Art, Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'poem_en',
            'poem_cn',
            'art_id'
        ]

# class RecordListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Record
#         fields = [
#             'id',
#         ]

class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = [
            'id',
            'image_binary',
        ]