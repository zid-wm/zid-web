from django.db import models


class Event(models.Model):
    name = models.TextField()
    host = models.TextField(null=True)
    fields = models.TextField(null=True)
    description = models.TextField(null=True)
    date = models.TextField()
    start_time = models.TextField()
    end_time = models.TextField()
    banner_path = models.TextField(null=True)
    status = models.IntegerField()
    reg = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
