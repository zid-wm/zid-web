from django.db import models


class Loa(models.Model):
    name = models.TextField()
    identifier = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
