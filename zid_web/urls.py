"""zid_home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from event import views as event
from pilots import views as pilots
from resources import views as resources
from uls import views as uls
from user import views as user
from views import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_home, name='home'),

    # Events
    path('events/', event.view_events, name='events'),
    path('events/new/', event.view_new_event, name='new-event'),
    path('events/archived/', event.view_archived_events, name='archived-events'),
    path('events/<int:event_id>', event.view_event_details, name='event-details'),
    path('events/<int:event_id>/delete-position/<int:position_id>',
         event.delete_position, name='delete-position'),

    # Pilots
    path('pilot-briefing/', pilots.view_pilot_briefing, name='briefing'),
    path('routes/', pilots.view_preferred_routes, name='routes'),
    path('request-event-staffing/', pilots.view_staffing_request,
         name='request-event-staffing'),

    # Resources
    path('files/', resources.view_files, name='files'),

    # ULS (Auth)
    path('login/', uls.login, name='login'),
    path('logout/', uls.logout, name='logout'),

    # User
    path('mavp/', user.view_mavp, name='mavp'),
    path('mavp/remove/<str:facility>', user.view_remove_mavp, name='remove-mavp'),
    path('roster/', user.view_roster, name='roster'),
    path('staff/', user.view_staff, name='staff'),
    path('statistics/', user.view_statistics, name='statistics')
]
