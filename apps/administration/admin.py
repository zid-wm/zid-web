from django.contrib import admin
from .models import ActionLog, MAVP


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action')


@admin.register(MAVP)
class MAVP(admin.ModelAdmin):
    list_display = ('facility_short', 'facility_long')
