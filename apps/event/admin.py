from django.contrib import admin
from apps.event.models import (
    Event,
    EventSignup,
    EventPosition,
    PositionPreset
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')


@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ('position', 'user')


@admin.register(EventPosition)
class EventPositionAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'callsign')


@admin.register(PositionPreset)
class PositionPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'positions_json')
