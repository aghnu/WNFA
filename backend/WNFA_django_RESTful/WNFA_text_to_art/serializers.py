from dataclasses import field
from rest_framework import serializers
from .models import Art, Record

class RecordSerializerGETorPOST(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'request_time',
            'poem_en',
            'poem_cn',
            'art_id'
        ]

class ArtSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = [
            'image_binary',
        ]