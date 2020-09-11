from django.db import models


class EventPositions(models.Model):
    event_id = models.ForeignKey(
        'Event', on_delete=models.CASCADE)
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
