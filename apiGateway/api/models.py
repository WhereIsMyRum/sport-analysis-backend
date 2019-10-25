from django.db import models
from django.utils import timezone

class UserStorage (models.Model) :
    user_id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    bucket_name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

class UserStorageEntries (models.Model) :
    user_storage = models.ForeignKey(UserStorage, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255, unique=True)
    uploaded = models.BooleanField(default=False)
    analyzed = models.BooleanField(default=False)
    clips_no = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    details = models.TextField(max_length=500, blank=True, null=True)

class UserStorageAnalyzedEntries (models.Model) :
    user_storage_entry = models.ForeignKey(UserStorageEntries, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255)
    uploaded = models.BooleanField(default=False)