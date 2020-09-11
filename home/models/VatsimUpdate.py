from django.db import models


class VatsimUpdate(models.Model):
    update_time = models.DateTimeField()
