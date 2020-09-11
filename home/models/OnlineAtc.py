from django.db import models


class OnlineAtc(models.Model):
    cid = models.IntegerField()
    name = models.TextField()
    position = models.TextField()
    freq = models.TextField()
    time_logon = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
