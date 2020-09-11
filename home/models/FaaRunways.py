from django.db import models


class FaaRunways(models.Model):
    runway_id = models.IntegerField(primary_key=True)
    site_number = models.ForeignKey('FaaFacilities', on_delete=models.CASCADE)
    runway_identifier = models.TextField()
    runway_length = models.TextField()
    runway_width = models.TextField()
    runway_surface_type_condition = models.TextField()
    base_end = models.TextField()
    base_end_heading = models.IntegerField()
    reciprocal_end = models.TextField()
    reciprocal_end_heading = models.IntegerField()
