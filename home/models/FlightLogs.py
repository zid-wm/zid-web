from django.db import models


class FlightLogs(models.Model):
    callsign = models.TextField()
    cid = models.TextField()
    real_name = models.TextField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)
    altitude = models.IntegerField()
    groundspeed = models.IntegerField()
    heading = models.IntegerField()
    planned_aircraft = models.TextField(null=True)
    planned_dep_airport = models.TextField(null=True)
    planned_dep_lat = models.DecimalField(
        max_digits=8, decimal_places=6, null=True)
    planned_dep_long = models.DecimalField(
        max_digits=9, decimal_places=6, null=True)
    planned_dest_airport = models.TextField(null=True)
    planned_dest_lat = models.DecimalField(
        max_digits=8, decimal_places=6, null=True)
    planned_dest_long = models.DecimalField(
        max_digits=9, decimal_places=6, null=True)
    planned_alt_airport = models.TextField(null=True)
    planned_alt_lat = models.DecimalField(
        max_digits=8, decimal_places=6, null=True)
    planned_alt_long = models.DecimalField(
        max_digits=9, decimal_places=6, null=True)
    planned_altitude = models.IntegerField(null=True)
    planned_flight_type = models.TextField(null=True)
    server = models.TextField()
    planned_revision = models.TextField(default='0')
    rating = models.TextField()
    planned_remarks = models.TextField()
    planned_route = models.TextField()
    state = models.IntegerField(default=0)
    missing = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    departure = models.DateTimeField(null=True)
    arrival = models.DateTimeField(null=True)
    logon = models.DateTimeField(null=True)
    seen_last = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
