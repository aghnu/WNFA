from copyreg import constructor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import BadRequest

from .models import Record, Art
from .serializers import RecordSerializer, ArtSerializer

from WNFA_text_to_art_generator.art_generator import ArtGeneratorFromImage
import base64

import json


class TicketSubmission(APIView):
    def post(self, request):
        try:
            record = None 
            art = None

            try:
                # generate art 
                img_base64 = request.data["data"]

                generator = ArtGeneratorFromImage(img_base64)
                img_gen_obj = generator.generate()
            except:
                raise BadRequest("Failed to generate Art")
            
            # create record and art
            try:
                art_new = Art(
                    data = img_gen_obj.image_bytes,
                    emotion_data = img_gen_obj.emotion_data
                )
                art_new.save()

                record_new = Record(
                    poem_en = img_gen_obj.text_en,
                    poem_cn = img_gen_obj.text_cn,
                    art_id = art_new.id
                )
                record_new.save()

                record = record_new
                art = art_new

            except:
                raise BadRequest("Failed to store Art or Record")

            return Response({'record_id': record.id}, status=status.HTTP_200_OK)
        
        except:
            raise BadRequest("Failed to process ticket")


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
            return Art.objects.get(id=art_id)
        except Art.DoesNotExist:
            raise Http404

    def get(self, request, art_id):
        art = self.get_art(art_id)
        art_base64 = base64.b64encode(art.data)
        print(art.emotion_data)
        emotion_data = json.loads(art.emotion_data)

        return Response({"id": art.id, "data": art_base64, "emotion_data": emotion_data}, status=status.HTTP_200_OK)