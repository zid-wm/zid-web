from django.db import models


class ZidField(models.Model):
    facility_id = models.TextField()
    site_number = models.ForeignKey('FaaFacilities', on_delete=models.CASCADE)
    location_id = models.CharField(max_length=4, primary_key=True)
    icao = models.TextField(null=True)
    apt_class = models.TextField(null=True)
    metar = models.IntegerField()
    atis = models.TextField(null=True)
    arrival_runways = models.TextField(null=True)
    departure_runways = models.TextField(null=True)
    approach = models.TextField(null=True)
    description = models.TextField(null=True)
    calm_wind_departure_runways = models.TextField(null=True)
    calm_wind_arrival_runways = models.TextField(null=True)
