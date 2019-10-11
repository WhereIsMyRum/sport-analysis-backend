from django.shortcuts import render
import requests, minio, subprocess, hashlib, datetime
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
        file_name = "uncut.mp4"
        print("penis")
        if (request.GET.get('fname')) :
            file_name = request.GET.get('fname')

        request_hardcoded={'user_id':1}

        try:
            storage_queryset = models.UserStorage.objects.get(user_id = request_hardcoded['user_id'])
        except :
            serializer = serializers.UserStorageSerializer()
            userstorage = serializer.create(request_hardcoded, settings.DEFAULT_BUCKET)
            subprocess.run(['mkdir -p /tmp'])
            subprocess.run(['touch /tmp/readme.txt'])
            with open ('readme.txt', 'rb') as file_data :
                file_stat = os.stat('/tmp/readme.txt')
                minioClient.put_object(settings.DEFAULT_BUCKET, "user_{}/readme.txt".format(request_hardcoded['user_id']), file_data, file_stat.st_size)
            subprocess.run(['rm /tmp/readme.txt'])
            storage_queryset = models.UserStorage.objects.get(user_id = request_hardcoded['user_id'])

        entry_folder_name = self.getUniqueFolderName(request_hardcoded['user_id'])

        try:
            serializer = serializers.UserStorageEntriesSerializer()
            storage_entry = serializer.create(storage_queryset, request_hardcoded['user_id'], entry_folder_name)  
        except :
            print("unable to create db entry")

        presigned = minioClient.presigned_put_object(settings.DEFAULT_BUCKET, "user_{}/{}/{}".format(request_hardcoded['user_id'], entry_folder_name, file_name))

        return Response(presigned)

    def getUniqueFolderName(self, user_id) :
        m = hashlib.md5()
        input_string = datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S') + str(user_id)
        m.update(input_string.encode('utf-8'))

        return m.hexdigest()