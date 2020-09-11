from django.db import models


class VisitRequests(models.Model):
    cid = models.IntegerField()
    name = models.TextField()
    email = models.TextField()
    rating = models.IntegerField()
    home = models.TextField()
    reason = models.TextField()
    status = models.IntegerField()
    reject_reason = models.TextField()
    updated_by = models.ForeignKey(
        'Roster', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
