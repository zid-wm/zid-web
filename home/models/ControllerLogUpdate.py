from django.db import models


class ControllerLogUpdate(models.Model):
    update_time = models.DateTimeField(auto_now=True)
