from django.db import models
from django.utils import timezone

class UserStorage (models.Model) :
    user_id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    bucket_name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

class UserStorageEntries (models.Model) :
    userstorage = models.ForeignKey(UserStorage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=200)
    uploaded = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=200, blank=True, null=True)