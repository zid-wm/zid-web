import json

from django.db import models

from apps.user.models import User


class Event(models.Model):
    name = models.CharField(max_length=128)
    banner = models.URLField(null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    host = models.CharField(max_length=16)
    description = models.TextField(null=True, blank=True)
    hidden = models.BooleanField(default=False)

    @property
    def duration(self):
        return self.end - self.start

    def __str__(self):
        return self.name


class EventPosition(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, related_name='positions')
    user = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True, related_name='event_positions')
    callsign = models.CharField(max_length=16)

    @property
    def category(self):
        if '_DEL' in self.callsign or '_GND' in self.callsign or '_TWR' in self.callsign:
            return 'cab'
        elif '_APP' in self.callsign or '_DEP' in self.callsign:
            return 'tracon'
        else:
            return 'center'


class EventSignup(models.Model):
    position = models.ForeignKey(
        EventPosition, models.CASCADE, related_name='signups')
    user = models.ForeignKey(User, models.CASCADE,
                             related_name='event_signups')

    def assign(self):
        self.position.user = self.user
        self.position.save()


class PositionPreset(models.Model):
    name = models.CharField(max_length=32)
    positions_json = models.TextField(default='[]')

    @property
    def positions(self):
        return json.loads(self.positions_json)

    def set_positions(self, positions):
        self.positions_json = json.dumps(positions)

    def add_to_event(self, event):
        for position in self.positions:
            EventPosition(
                event=event,
                user=None,
                callsign=position,
            ).save()

    def __str__(self):
        return self.name
