from django.db import models


class AirportWeather(models.Model):
    icao = models.TextField()
    metar = models.TextField(null=True)
    taf = models.TextField(null=True)
    visual_conditions = models.TextField(null=True)
    altimeter = models.TextField(null=True)
    wind = models.TextField(null=True)
    temp = models.TextField(null=True)
    dp = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
