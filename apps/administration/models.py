from django.db import models
from apps.user.models import User


class ActionLog(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp} | {self.action}'


class MAVP(models.Model):
    facility_short = models.CharField(max_length=16)
    facility_long = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.facility_long} ({self.facility_short})'


class StaffComment(models.Model):
    writer = models.ForeignKey(User, models.CASCADE, related_name='writer')
    subject = models.ForeignKey(User, models.CASCADE, related_name='subject')
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
