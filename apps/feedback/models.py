from django.db import models

from apps.feedback.forms import SERVICE_LEVEL_CHOICES
from apps.user.models import User


STATUSES = (
    (0, 'Pending'),
    (1, 'Posted'),
    (2, 'Rejected')
)


class Feedback(models.Model):
    controller = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=16)
    service_level = models.IntegerField(choices=SERVICE_LEVEL_CHOICES)
    flight_callsign = models.CharField(max_length=16)
    pilot_name = models.CharField(max_length=64, null=True, blank=True)
    pilot_email = models.EmailField(max_length=255, null=True, blank=True)
    pilot_cid = models.CharField(max_length=16, null=True, blank=True)
    additional_comments = models.TextField(null=True, blank=True)

    submitted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    status = models.IntegerField(default=0, choices=STATUSES)
    staff_comment = models.TextField(null=True, blank=True)
