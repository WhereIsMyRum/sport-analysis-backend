from utils.c_rabbitWrapper import c_rabbitWrapper
import utils.utils as utils
import json, re, time, subprocess, os, threading, concurrent.futures
from math import ceil

class c_videoformatter(c_rabbitWrapper) :

    threadExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    minioClient = utils.getMinioClient()

    def callback(self, ch, method, properties, body):
        print("received new msg")
        
        body = json.loads(body.decode('utf-8'))

        file_location = utils.getBucketUserFolderAndFileFromPath(body['path'])

        self.createDirectories(file_location['folder'])

        self.threadExecutor.map(self.saveVideo, [file_location])
        time.sleep(1)

        self.cutVideo(body['cut_out'], file_location)

    def cutVideo(self, time_periods, file_location) :
        keys = [time_periods[key] for key in time_periods]
        file_location = [file_location for i in range(len(keys))]
        lock = [True for i in range(len(keys))]
        self.threadExecutor.map(self.cutSaveAndPublish, keys, file_location, lock)

    def cutSaveAndPublish(self, start_end, file_location, lock=False) :

        if lock :
            while (os.path.exists('/tmp/{}/lock'.format(file_location['folder']))):
                time.sleep(3)

        start_ffmpeg = utils.convertTimeToHMS(start_end["start"])
        end_ffmpeg = utils.convertTimeToHMS(str(float(start_end["end"])-float(start_end["start"])))
        output_file = '/tmp/{}/cut/video_{}_{}.mp4'.format(file_location['folder'], start_end["start"], start_end["end"])

        pcode = subprocess.call(['ffmpeg', '-v', 'quiet', '-y', '-i', 
                         '/tmp/{}/video_uncut.mp4'.format(file_location['folder']),
                         '-vcodec', 'copy', '-acodec', 'copy', '-ss', start_ffmpeg, '-t', end_ffmpeg, '-sn',
                         output_file])

        if (pcode == 0) :
            try :
                with open(output_file, 'rb') as vid:

                    self.minioClient.put_object(file_location['bucket'],
                                                file_location['user'] + '/' + file_location['folder'] + '/cut/' + 'video_{}_{}.mp4'.format(start_end['start'],start_end['end']),
                                                vid,
                                                os.stat(output_file).st_size)
            except Exception as e:
                print(e)




    def createDirectories(self, folder_name) :
        if (not os.path.isdir('/tmp/{}/cut'.format(folder_name))) :
            subprocess.run(['mkdir','-p', '/tmp/{}/cut'.format(folder_name)])

    def saveVideo(self, file_location) :
        subprocess.run(['touch', '/tmp/{}/lock'.format(file_location['folder'])])
        file_path = file_location['user'] + '/' + file_location['folder'] + '/' + file_location['file']
        utils.getVideoFromBucket(file_location['bucket'], file_path, '/tmp/{}/video_uncut.mp4'.format(file_location['folder']))
        subprocess.Popen(['rm', '/tmp/{}/lock'.format(file_location['folder'])])
