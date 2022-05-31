from dataclasses import field
from rest_framework import serializers
from .models import Art, Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'poem_en',
            'poem_cn',
            'art_id',
            'request_time',
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
            'data',
            'emotion_data'
        ]