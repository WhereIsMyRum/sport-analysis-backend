from utils.c_rabbitWrapper import c_rabbitWrapper
import utils.utils as utils
import json, re, time, subprocess, os, threading, concurrent.futures

class c_videoanalyzer(c_rabbitWrapper) :
    threadExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    minioClient = utils.getMinioClient()

    def callback(self, ch, method, properties, body):
        body = body.decode('utf-8')

        self.threadExecutor.map(self.saveAnalyzePublish, [body])


    def analyzeVideo(self) :
        result = {
            "cut_out":{
                "first" : {
                    "start" : 0,
                    "end" : 120
                },
                "second" : {
                    "start" : 120,
                    "end" : 240
                },
                "third" : {
                    "start" : 240,
                    "end" : 360
                },
                "fourth" : {
                    "start" : 360,
                    "end" : 480
                },
                "fifth" : {
                    "start" : 480,
                    "end" : 600
                }
            }
        }

        return result

    def saveAnalyzePublish(self, body):

        temp_mq_connection = c_videoanalyzer()

        file_location = utils.getBucketUserFolderAndFileFromPath(body)
        if (not os.path.isdir('/tmp/{}'.format(file_location['folder']))) :
            subprocess.run(['mkdir', '-p', '/tmp/{}'.format(file_location['folder'])])

        file_path = file_location['user'] + '/' + file_location['folder'] + '/' + file_location['file']
        utils.getVideoFromBucket(file_location['bucket'], file_path, '/tmp/{}/video_uncut.mp4'.format(file_location['folder']))
        time_periods = self.analyzeVideo()
        time_periods['path'] = body

        temp_mq_connection.publish(exchange='', routing_key="video_formatter_queue", body=json.dumps(time_periods))
        temp_mq_connection.close()

        subprocess.Popen(['rm -r', '/tmp/{}'.format(file_location['folder'])])

