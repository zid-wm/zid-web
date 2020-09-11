from django.db import models


class ControllerLog(models.Model):
    cid = models.IntegerField()
    name = models.TextField()
    position = models.TextField()
    duration = models.TextField()
    date = models.TextField()
    time_logon = models.TextField()
    stream_update = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
