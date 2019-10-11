import json, re, MySQLdb
from utils.c_rabbitWrapper import c_rabbitWrapper
from utils.utils import *
from datetime import datetime

class c_msgdispatcher(c_rabbitWrapper) :

    def callback(self, ch, method, properties, body) :
        
        body_js = json.loads(body.decode('utf-8'))
        if (re.search(EVENT_NAME, body_js['EventName'])) :
            if (re.search(INITIAL_KEY, body_js['Key'])) :
                self.publish(exchange='',routing_key='video_analyzer_queue', body=body_js['Key'])
                self.updateUserStorageEntries(body_js['Key'])
            if (re.search(RESULT_KEY, body_js['Key'])) :
                print("uploaded cut videos")
    
    def extractBucketRelativePath(self, key) :
        return re.search(INITIAL_KEY, key).group(1)

    def getDBConnection(self) :
        db = MySQLdb.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, db="db")
        return db

    def updateUserStorageEntries(self, key) :
        db = self.getDBConnection()
        bucketRelPath = self.extractBucketRelativePath(key)

        cursor = db.cursor()
        cursor.execute("UPDATE api_userstorageentries SET uploaded=1 WHERE path='{}'".format(
                        bucketRelPath
        ))
        db.commit()
