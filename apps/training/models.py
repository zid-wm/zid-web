from django.core.validators import MaxValueValidator
from django.db import models

from apps.user.models import User


SESSION_LOCATIONS = (
    (0, 'Classroom'),
    (1, 'Live'),
    (2, 'Sweatbox')
)


OTS_STATUSES = (
    (0, 'Not OTS'),
    (1, 'OTS Pass'),
    (2, 'OTS Fail'),
    (3, 'OTS Recommended')
)


PROGRESS_CHOICES = (
    (1, '1 - No Progress'),
    (2, '2 - Little Progress'),
    (3, '3 - Average Progress'),
    (4, '4 - Great Progress'),
    (5, '5 - Excellent Progress')
)


class TrainingTicket(models.Model):
    student = models.ForeignKey(User, models.CASCADE, related_name='student')
    instructor = models.ForeignKey(User, models.SET_NULL, related_name='instructor', null=True, blank=True)
    session_date = models.DateTimeField()
    position = models.CharField(max_length=16)
    session_duration = models.DurationField()
    movements = models.IntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(choices=PROGRESS_CHOICES)
    notes = models.TextField()
    location = models.IntegerField(choices=SESSION_LOCATIONS)
    ots_status = models.IntegerField(default=0, choices=OTS_STATUSES, null=True, blank=True)
    solo_granted = models.BooleanField(default=False)
    vatusa_id = models.IntegerField(null=True, blank=True)
