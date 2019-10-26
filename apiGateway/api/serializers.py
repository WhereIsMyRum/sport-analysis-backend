from rest_framework import serializers, exceptions
from api.models import UserStorage, UserStorageEntries, UserStorageAnalyzedEntries
from django.utils import timezone
import datetime

class UserStorageSerializer(serializers.ModelSerializer) :
    class Meta:
        model = UserStorage
        fields = ('user_id','created','path')
        extra_kwargs = {'created' : {'read_only':True},
                        'user_id':{'read_only':True},
                        }

    def create(self, request, bucket_name) :
        userstorage = UserStorage()

        userstorage.user_id = request.data['user_id']
        userstorage.created = datetime.datetime.utcnow()
        userstorage.bucket_name = bucket_name
        userstorage.path='user_{}'.format(userstorage.user_id)

        userstorage.save()

        return userstorage


class UserStorageEntriesSerializer(serializers.ModelSerializer) :
    storage = UserStorage()

    class Meta:
        model = UserStorageEntries
        fields = ('id','created','title','details')
    
    def create(self,request, storage, entry_folder) :
        storageentry = UserStorageEntries()

        storageentry.created=datetime.datetime.utcnow()
        storageentry.path="user_{}/{}".format(request.data['user_id'], entry_folder)
        storageentry.title = request.data['title']
        storageentry.user_storage=storage
        storageentry.analyzed=0
        storageentry.clips_no=0

        if 'details' in request.data :
            storageentry.details = request.data['details']
        else :
            storageentry.details = ''


        storageentry.save()
        return storageentry

class UserStorageAnalyzedEntriesSerializer(serializers.ModelSerializer) :
    storage_entry = UserStorageEntries()

    class Meta:
        model = UserStorageAnalyzedEntries
        fields = ('created','path','label')
