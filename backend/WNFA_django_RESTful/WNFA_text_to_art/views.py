from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import BadRequest

from .models import Record, Art
from .serializers import RecordSerializer, ArtSerializer

class RecordList(APIView):
    def get(self, request):
        select = request.query_params.get("select", None)
        if select != None:
            try: 
                select = int(select)
            except:
                raise BadRequest("The key of select must be an integer")

            try:
                record = Record.objects.all().order_by('-request_time')[select]
            except Record.DoesNotExist:
                raise Http404
            except IndexError:
                raise Http404

            serializer = RecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        else:
            records = Record.objects.all()
            serializer = RecordSerializer(records, many=True)
            return Response(
                {'total':len(serializer.data), 'records':serializer.data},
                status=status.HTTP_200_OK)            

    def post(self, request):
        serializer = RecordSerializer(data=request.data)
        
        # mock art generator process for testing
        new_art = Art(image_binary = bytes())
        new_art.save()

        request.data.update({"art_id": new_art.id})
        # the end of mock

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

class ArtList(APIView):
    def get(self, request):
        arts = Art.objects.all()
        serializer = ArtSerializer(arts, many=True)
        return Response(
            {'total':len(serializer.data), 'arts':serializer.data},
            status=status.HTTP_200_OK)            

class ArtDetail(APIView):
    def get_art(self, art_id):
        try:
            print(Art.objects.get(id=art_id))
        except Art.DoesNotExist:
            raise Http404

    def get(self, request, art_id):
        art = self.get_art(art_id)
        serializer = ArtSerializer(art)
        return Response(serializer.data, status=status.HTTP_200_OK)