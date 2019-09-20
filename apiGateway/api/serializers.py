from rest_framework import serializers, exceptions
from api.models import UserStorage, UserStorageEntries
from django.utils import timezone

class UserStorageSerializer(serializers.ModelSerializer) :
    class Meta:
        model = UserStorage
        fields = ('user_id','created','path')
        extra_kwargs = {'created' : {'read_only':True},
                        'user_id':{'read_only':True},
                        }

    def create(self, request, bucket_name) :
        userstorage = UserStorage()

        userstorage.user_id = request['user_id']
        userstorage.created = timezone.now()
        userstorage.bucket_name = bucket_name
        userstorage.path='user_{}'.format(userstorage.user_id)

        userstorage.save()

        return userstorage
        
class UserStorageEntriesSerializer(serializers.ModelSerializer) :
    storage = UserStorage()

    class Meta:
        model = UserStorageEntries
        fields = ('id','created','path','title','storage')
    
    def create(self,storage,user_id,entry_id) :
        storageentry = UserStorageEntries()

        storageentry.created=timezone.now()
        storageentry.path="user_{}/entry_{}".format(user_id, entry_id)
        storageentry.title = "Title"
        storageentry.storage=storage

        storageentry.save()
        return storageentry