from django.db import models


class Calendar(models.Model):
    title = models.TextField()
    date = models.TextField()
    time = models.TextField(null=True)
    body = models.TextField()
    entry_type = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
