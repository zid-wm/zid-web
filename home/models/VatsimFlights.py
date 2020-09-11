from django.db import models


class VatsimFlights(models.Model):
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
    planned_dest_airport = models.TextField(null=True)
    planned_alt_airport = models.TextField(null=True)
    planned_altitude = models.IntegerField(null=True, default=0)
    planned_flight_type = models.TextField(null=True)
    server = models.TextField()
    planned_revision = models.TextField(default='0')
    rating = models.TextField()
    planned_remarks = models.TextField()
    planned_route = models.TextField()
    time_logon = models.DateTimeField()
