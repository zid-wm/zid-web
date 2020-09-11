from django.db import models


class ZidFaaFields(models.Model):
    site_number = models.ForeignKey('FaaFacilities', on_delete=models.CASCADE)
    location_id = models.TextField()
