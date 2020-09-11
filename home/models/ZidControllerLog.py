from django.db import models


class ZidControllerLog(models.Model):
    callsign = models.TextField()
    cid = models.TextField()
    real_name = models.TextField()
    frequency = models.TextField(default='199.998')
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)
    server = models.TextField()
    rating = models.TextField()
    facility_type = models.IntegerField()
    vis_range = models.TextField()
    atis_message = models.TextField(null=True)
    time_last_atis_received = models.TextField(null=True)
    logon = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    seen_last = models.DateTimeField(auto_now=True)
