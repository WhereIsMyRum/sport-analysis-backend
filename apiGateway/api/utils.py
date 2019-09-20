from django.conf import settings
import minio

def getMinioClient() :
    minioClient = minio.Minio('s3.docker:9000',
                            access_key=settings.S3_ACCESS_KEY,
                            secret_key=settings.S3_SECRET_KEY,
                            secure=False)

    return minioClient
