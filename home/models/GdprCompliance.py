from django.db import models


class GdprCompliance(models.Model):
    controller_id = models.ForeignKey('Roster', on_delete=models.CASCADE)
    option = models.IntegerField()
    ip_address = models.CharField(max_length=15)
    means = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
