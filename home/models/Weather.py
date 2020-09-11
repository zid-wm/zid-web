from django.db import models


class Weather(models.Model):
    icao = models.CharField(max_length=4, primary_key=True)
    metar = models.TextField()
    observation_time = models.DateTimeField()
    taf = models.TextField(null=True)
    flight_rules = models.TextField()
    wind = models.TextField()
    altimeter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
