from django.shortcuts import render
import requests, minio, os
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api import utils, models, serializers
from django.conf import settings


# Create your views here.

class UploadView(APIView) :
    permission_class = [AllowAny]

    def get(self, request) :
        minioClient = utils.getMinioClient()

        request_hardcoded={'user_id':1}
        try:
            storage_queryset = models.UserStorage.objects.get(user_id = request_hardcoded['user_id'])
        except :
            serializer = serializers.UserStorageSerializer()
            userstorage = serializer.create(request_hardcoded, settings.DEFAULT_BUCKET)
            os.system('touch readme.txt')
            with open ('readme.txt', 'rb') as file_data :
                file_stat = os.stat('readme.txt')
                minioClient.put_object(settings.DEFAULT_BUCKET, "user_{}/readme.txt".format(request_hardcoded['user_id']), file_data, file_stat.st_size)
            os.system('rm readme.txt')
        
        try:
            entries_queryset = models.UserStorageEntries.objects.filter(storage_id = storage_queryset.user_id)
            serializer = serializers.UserStorageEntriesSerializer()
            subfolder_entry_id = len(entries_queryset) + 1
            storage_entry = serializer.create(storage_queryset,request_hardcoded['user_id'],subfolder_entry_id)

        except :
            serializer = serializers.UserStorageEntriesSerializer()
            subfolder_entry_id = 1
            storage_entry = serializer.create(storage_queryset,request_hardcoded['user_id'],subfolder_entry_id)

        presigned = minioClient.presigned_put_object(settings.DEFAULT_BUCKET, "vid")

        return Response(presigned)