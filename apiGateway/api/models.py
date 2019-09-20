from django.db import models

class UserStorage (models.Model) :
    user_id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    bucket_name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

class UserStorageEntries (models.Model) :
    storage = models.ForeignKey(UserStorage, on_delete=models.CASCADE)
    created = models.DateTimeField()
    path = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=200, blank=True, null=True)