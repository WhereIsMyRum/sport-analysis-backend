import minio, re, time
from math import ceil

S3_ACCESS_KEY = "admin"
S3_SECRET_KEY = "password"

RESULT_KEY = r"\/user_[0-9]*\/[a-z0-9]*\/cut\/[a-zA-Z0-9-_]*.(mp4|vid)$"
INITIAL_KEY = r"\/(user_[0-9]*\/[a-z0-9]*)\/[a-zA-Z-_]*.mp4$"
EVENT_NAME = "ObjectCreated:Put"

DB_HOST = 'db.internal'
DB_USERNAME = 'root'
DB_PASSWORD = 'password'

def getMinioClient() :
    minioClient = minio.Minio('s3.docker:9000',
                            access_key=S3_ACCESS_KEY,
                            secret_key=S3_SECRET_KEY,
                            secure=False)

    return minioClient

def getBucketUserFolderAndFileFromPath(path) :
    match = re.search(r'^([a-zA-Z0-9-_]*)\/(user_[0-9]*)\/([a-zA-Z0-9]*)(\/cut)?\/(.*)$', path)
    file_location = {
        'bucket': match.group(1),
        'user': match.group(2),
        'folder': match.group(3),
        'file': match.group(5)
    }
    return file_location

def convertTimeToHMS(time, format='s') :
    time = int(ceil(float(time)))
    if (format == 's') :
        seconds = time % 60
        minutes = int(((time - seconds) / 60) % 60)
        hours = int(((time - seconds) / 60) / 60)
    elif (format == 'm') :
        seconds = 0
        minutes = int(time % 60)
        hours = int(time/60)
    elif (format == 'h') :
        seconds = 0
        minutes = 0
        hours = time
    else :
        pass

    return ("{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds))


def getVideoFromBucket(bucket, file_path, file_name='/tmp/video_uncut.mp4') :
    minioClient = getMinioClient()
    video = minioClient.get_object(bucket, file_path)

    with open(file_name, 'wb') as file_data :
        for d in video.stream() :
            file_data.write(d)
    return video

def getFolderNameFromPath(file_path) :
    folder_name = re.search(r'user_[0-9]*\/([a-z0-9]*)\/',file_path).group(1)
    return folder_name