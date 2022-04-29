from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Record, Art
from .serializers import RecordSerializer, ArtSerializer

class RecordList(APIView):
    def post(self, request):
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

class RecordDetail(APIView):
    def get_record(self, record_id):
        try:
            return Record.objects.get(id=record_id)
        except Record.DoesNotExist:
            raise Http404

    def get(self, request, record_id):
        record = self.get_record(record_id)
        serializer = RecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)