from django.db import models


class VatsimPrefiled(models.Model):
    callsign = models.TextField()
    cid = models.TextField()
    real_name = models.TextField()
    planned_aircraft = models.TextField(null=True)
    planned_dep_airport = models.TextField(null=True)
    planned_dest_airport = models.TextField(null=True)
    planned_alt_airport = models.TextField(null=True)
    planned_altitude = models.IntegerField(null=True)
    planned_flight_type = models.TextField(null=True)
    rating = models.TextField()
    planned_remarks = models.TextField(null=True)
    planned_route = models.TextField(null=True)
