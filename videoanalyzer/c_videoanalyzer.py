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
            "cut_out":[
                {
                    "label": "'backhand'",
                    "value": 4.2042042042042045
                },
                {
                    "label": "'serv_toss'",
                    "value": 25.759092425759093
                },
                {
                    "label": "'serv_toss'",
                    "value": 26.426426426426428
                },
                {
                    "label": "'serv_toss'",
                    "value": 29.42942942942943
                },
                {
                    "label": "'serv_toss'",
                    "value": 31.43143143143143
                },
                {
                    "label": "'serv_toss'",
                    "value": 31.7650984317651
                },
                {
                    "label": "'serv_toss'",
                    "value": 32.098765432098766
                },
                {
                    "label": "'serv_smash'",
                    "value": 32.7660994327661
                },
                {
                    "label": "'serv_toss'",
                    "value": 55.12178845512179
                },
                {
                    "label": "'serv_toss'",
                    "value": 55.45545545545546
                },
                {
                    "label": "'serv_toss'",
                    "value": 55.789122455789126
                },
                {
                    "label": "'serv_smash'",
                    "value": 56.12278945612279
                },
                {
                    "label": "'serv_toss'",
                    "value": 58.1247914581248
                },
                {
                    "label": "'serv_toss'",
                    "value": 65.79913246579913
                },
                {
                    "label": "'serv_toss'",
                    "value": 66.1327994661328
                },
                {
                    "label": "'serv_smash'",
                    "value": 66.46646646646647
                },
                {
                    "label": "'serv_smash'",
                    "value": 66.80013346680013
                },
                {
                    "label": "'backhand'",
                    "value": 68.80213546880213
                },
                {
                    "label": "'backhand'",
                    "value": 69.13580246913581
                },
                {
                    "label": "'serv_toss'",
                    "value": 97.4974974974975
                },
                {
                    "label": "'serv_toss'",
                    "value": 99.16583249916583
                },
                {
                    "label": "'serv_toss'",
                    "value": 99.4994994994995
                },
                {
                    "label": "'serv_toss'",
                    "value": 99.83316649983317
                },
                {
                    "label": "'serv_toss'",
                    "value": 103.16983650316985
                },
                {
                    "label": "'serv_toss'",
                    "value": 103.83717050383717
                },
                {
                    "label": "'serv_toss'",
                    "value": 104.17083750417085
                },
                {
                    "label": "'serv_toss'",
                    "value": 106.50650650650651
                },
                {
                    "label": "'serv_toss'",
                    "value": 106.84017350684017
                },
                {
                    "label": "'serv_smash'",
                    "value": 107.17384050717385
                },
                {
                    "label": "'serv_smash'",
                    "value": 107.50750750750751
                },
                {
                    "label": "'serv_toss'",
                    "value": 134.8682015348682
                },
                {
                    "label": "'serv_toss'",
                    "value": 135.20186853520187
                },
                {
                    "label": "'serv_toss'",
                    "value": 135.53553553553553
                },
                {
                    "label": "'serv_smash'",
                    "value": 135.86920253586922
                },
                {
                    "label": "'serv_smash'",
                    "value": 136.20286953620288
                },
                {
                    "label": "'forhand'",
                    "value": 188.25492158825492
                },
                {
                    "label": "'serv_toss'",
                    "value": 310.0433767100434
                },
                {
                    "label": "'serv_toss'",
                    "value": 310.37704371037705
                },
                {
                    "label": "'serv_toss'",
                    "value": 310.7107107107107
                },
                {
                    "label": "'serv_toss'",
                    "value": 311.37804471137804
                },
                {
                    "label": "'serv_toss'",
                    "value": 311.7117117117117
                },
                {
                    "label": "'backhand'",
                    "value": 330.0633967300634
                },
                {
                    "label": "'forhand'",
                    "value": 501.9019019019019
                },
                {
                    "label": "'backhand'",
                    "value": 504.2375709042376
                },
                {
                    "label": "'backhand'",
                    "value": 504.57123790457126
                },
                {
                    "label": "'backhand'",
                    "value": 506.57323990657324
                },
                {
                    "label": "'backhand'",
                    "value": 638.2716049382716
                }
                ]}

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

