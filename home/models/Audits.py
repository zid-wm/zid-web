from django.db import models


class Audits(models.Model):
    cid = models.ForeignKey('Roster', on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    what = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
