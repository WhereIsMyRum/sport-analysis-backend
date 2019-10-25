from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
import requests, minio, subprocess, hashlib, datetime
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api import utils, models, serializers
from django.conf import settings


# Create your views here.

class UploadView(APIView) :
    permission_class = [AllowAny]
    minioClient = utils.getMinioClient()

    def post(self, request) :
        file_name = "video.mp4"

        if not self.validate_request() :
            return Response({"user_id":"This field cannot be empty", "title":"This field cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            storage_queryset = models.UserStorage.objects.get(user_id = request.data['user_id'])
        except :
            serializer = serializers.UserStorageSerializer()
            serializer.create(request, settings.DEFAULT_BUCKET)
            storage_queryset = models.UserStorage.objects.get(user_id = request.data['user_id'])

        entry_folder_name = self.getUniqueFolderName(request.data['user_id'])

        serializer = serializers.UserStorageEntriesSerializer()
        serializer.create(request, storage_queryset, entry_folder_name)

        presigned = self.minioClient.presigned_put_object(settings.DEFAULT_BUCKET, "user_{}/{}/{}".format(request.data['user_id'], entry_folder_name, file_name))

        return Response({"data":{"upload_url":presigned}}, status=status.HTTP_201_CREATED)

    def getUniqueFolderName(self, user_id) :
        m = hashlib.md5()
        input_string = datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S') + str(user_id)
        m.update(input_string.encode('utf-8'))

        return m.hexdigest()

    def validate_request(self) :
        if 'user_id' in self.request.data and 'title' in self.request.data :
            return True
        else :
            return False

class GamesView(ListAPIView) :
    permission_classes = [AllowAny]
    serializer_class = serializers.UserStorageEntriesSerializer

    def list(self, request) :
        queryset = self.get_queryset()
        serializer = serializers.UserStorageEntriesSerializer(queryset, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

    def get_queryset(self) :
        queryset = models.UserStorageEntries.objects.filter(user_storage_id=self.request.data['user_id'], analyzed=1)
        
        return queryset

class GamesDetailedView(ListAPIView) :
    permission_classes = [AllowAny]
    serializer_class = serializers.UserStorageAnalyzedEntriesSerializer
    minioClient = utils.getMinioClient()

    def list(self, request, pk=None) :
        queryset = self.get_queryset()
        serializer = serializers.UserStorageAnalyzedEntriesSerializer(queryset, many=True)
        response_data = []

        for data in serializer.data :
            modified_response_data = {}
            modified_response_data['created'] = data['created']
            modified_response_data['label'] = data['label']
            modified_response_data['download_url'] = self.minioClient.presigned_get_object(settings.DEFAULT_BUCKET, data['path'])
            response_data.append(modified_response_data)
        print(response_data)

        return Response({"data":response_data}, status=status.HTTP_200_OK)

    def get_queryset(self) :
        queryset = models.UserStorageAnalyzedEntries.objects.filter(user_storage_entry_id = self.kwargs['pk'], uploaded=1)

        return queryset