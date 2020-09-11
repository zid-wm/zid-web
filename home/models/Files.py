from django.db import models


class Files(models.Model):
    name = models.TextField()
    file_type = models.IntegerField()
    desc = models.TextField(null=True)
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
