from django.shortcuts import render
import requests, minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


# Create your views here.

class UploadView(APIView) :
    permission_classe = [AllowAny]

    def get(self, request) :
        minioClient = minio.Minio('s3.docker:9000',
                                access_key="password",
                                secret_key="password",
                                secure=False)
        try:
            buckets = minioClient.make_bucket("testbuck");
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            Response(err)

        #r = requests.get("http://s3:9000")
        #response = {
        #    "status": r.status_code,
        #    "body" : r.text,
        #}

        return Response(buckets)