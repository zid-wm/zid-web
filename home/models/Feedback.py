from django.db import models


class Feedback(models.Model):
    controller_id = models.ForeignKey('Roster', on_delete=models.CASCADE)
    position = models.TextField()
    service_level = models.IntegerField()
    callsign = models.TextField()
    pilot_name = models.TextField(null=True)
    pilot_email = models.TextField(null=True)
    pilot_cid = models.IntegerField(null=True)
    comments = models.TextField(null=True)
    staff_comments = models.TextField(null=True)
    status = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
