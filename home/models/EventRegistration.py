from django.db import models


class EventRegistration(models.Model):
    event_id = models.ForeignKey(
        'Event', on_delete=models.CASCADE)

    # TODO: Add additional foreign key relationships?
    controller_id = models.IntegerField()

    # TODO do we want to cascade here?
    position_id = models.ForeignKey(
        'EventPositions', on_delete=models.CASCADE)
    start_time = models.TextField(null=True)
    end_time = models.TextField(null=True)
    status = models.IntegerField()
    choice_number = models.IntegerField()
    reminder = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
