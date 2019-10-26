import json, re, MySQLdb
from utils.c_rabbitWrapper import c_rabbitWrapper
from utils.utils import *
from datetime import datetime
from math import floor

class c_msgdispatcher(c_rabbitWrapper) :
    minioClient = getMinioClient()

    def callback(self, ch, method, properties, body) :

        body_js = json.loads(body.decode('utf-8'))
        try :
            if (re.search(EVENT_NAME, body_js['EventName'])) :
                if (re.search(INITIAL_KEY, body_js['Key'])) :
                    self.publish(exchange='',routing_key='video_analyzer_queue', body=body_js['Key'])
                    self.dbUpdate('api_userstorageentries', 'uploaded=1', "path='{}'".format(self.extractBucketRelativePath(body_js['Key'])))
                    print("uploaded new video")

                if (re.search(RESULT_KEY, body_js['Key'])) :
                    path = getBucketUserFolderAndFileFromPath(body_js['Key'])
                    query_result = self.dbGet('api_userstorageentries', 'id, clips_no', "path='{}'".format(path['user']+"/"+path['folder']))
                    original_video_id, expected_number_of_clips = query_result[0]
                    pref = path['user'] + "/" + path['folder'] + "/cut"
                    objects = self.minioClient.list_objects('tennis-video-bucket-1', prefix=pref,  recursive=True)
                    actual_number_of_clips = sum(1 for _ in objects)
                    self.dbUpdate('api_userstorageanalyzedentries', f"uploaded=1", "path='{}'".format(path['user']+"/"+path['folder']+"/cut/"+path['file']))
                    if (expected_number_of_clips == actual_number_of_clips) :
                        self.dbUpdate('api_userstorageentries', 'analyzed=1', "path='{}'".format(path['user']+"/"+path['folder']))

        except Exception as ex:
            db, close_connection = self.getDBConnection(None)
            path = self.extractBucketRelativePath(body_js['path'])
            self.dbUpdate('api_userstorageentries',f"clips_no={len(body_js['cut_out'])}","path='{}'".format(path), db)
            original_video_id = self.dbGet('api_userstorageentries', 'id', "path='{}'".format(path), db)[0][0]
            for cut_video in body_js['cut_out'] :
                try :
                    self.dbInsert('api_userstorageanalyzedentries', [[datetime.utcnow(),path + "/cut/" + cut_video['label'][1:-1] +'-'+str(floor(cut_video['value']))+".mp4",
                                cut_video['label'][1:-1],original_video_id, 0]], ['created','path','label','user_storage_entry_id', 'uploaded'], db)
                except MySQLdb._exceptions.IntegrityError as ex :
                    pass
            self.publish(exchange='', routing_key="video_formatter_queue", body=json.dumps(body_js))

    def extractBucketRelativePath(self, key) :
        return re.search(INITIAL_KEY, key).group(1)

    def getDBConnection(self,db) :
        if db is None :
            db = MySQLdb.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, db="db")
            close_connection = True
        else :
            close_connection = False

        return db, close_connection

    def dbUpdate(self, table, set_val, where, db = None) :
        db, close_connection = self.getDBConnection(db)
        cursor = db.cursor()
        print(f"UPDATE {table} SET {set_val} WHERE {where}")
        cursor.execute(f"UPDATE {table} SET {set_val} WHERE {where}")
        db.commit()

        if close_connection :
            cursor.close()
            db.close()
        else :
            cursor.close()

    def dbGet(self, table, select, where='', db = None) :
        db, close_connection = self.getDBConnection(db)
        cursor = db.cursor()
        if not where :
            cursor.execute(f"SELECT {select} FROM {table}")
        else :
            cursor.execute(f"SELECT {select} FROM {table} WHERE {where}")

        query_result = cursor.fetchall()

        if close_connection :
            cursor.close()
            db.close()
        else :
            cursor.close()

        return query_result

    def dbInsert(self, table, values_list, columns=None, db = None) :
        db, close_connection = self.getDBConnection(db)

        cursor = db.cursor()
        insert_values = ""
        for values in values_list :
            single_entry = "("
            for value in values :
                single_entry += f"'{value}',"
            single_entry = single_entry[0:-1]
            single_entry += "),"
        insert_values += single_entry
        insert_values = insert_values[0:-1]
        if not columns :
            cursor.execute(f"INSERT INTO {table} VALUES {insert_values}")
        else :
            columns_list = "("
            for column in columns :
                columns_list += f"{column},"
            columns_list = columns_list[0:-1]
            columns_list += ")"

            cursor.execute(f"INSERT INTO {table} {columns_list} VALUES {insert_values}")
        db.commit()

        if close_connection :
            cursor.close()
            db.close()
        else :
            cursor.close()

