from django.db import models


class ZidFacilities(models.Model):
    facility_id = models.TextField(primary_key=True)
    primary_airport = models.TextField()
    full_name = models.TextField()
    facility_type = models.TextField()
    active = models.IntegerField()
