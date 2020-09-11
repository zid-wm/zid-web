from django.db import models


class Airports(models.Model):
    name = models.TextField()
    front_pg = models.IntegerField(default=0)
    ltr_4 = models.CharField(max_length=4)
    ltr_3 = models.CharField(max_length=3)
