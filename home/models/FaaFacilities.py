from django.db import models


class FaaFacilities(models.Model):
    site_number = models.CharField(max_length=15, primary_key=True)
    facility_type = models.TextField()
    location_id = models.TextField()
    city = models.TextField()
    state = models.TextField()
    facility_name = models.TextField()
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.FloatField()
    use = models.TextField()
    traffic_pattern_altitude = models.IntegerField(null=True)
    boundary_artcc_id = models.TextField()
    responsible_artcc_id = models.TextField(null=True)
    atct = models.TextField()
    icao_identifier = models.TextField()
