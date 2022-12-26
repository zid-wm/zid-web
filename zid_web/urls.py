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
from django.urls import path

from apps.administration import views as administration
from apps.api import views as api
from apps.event import views as event
from apps.feedback import views as feedback
from apps.news import views as news
from apps.pilots import views as pilots
from apps.resources import views as resources
from apps.sso import views as sso
from apps.training import views as training
from apps.user import views as user
from apps.views import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_home, name='home'),
    path('privacy-policy/', views.view_privacy_policy, name='privacy-policy'),

    # Administration
    path('audit-log/', administration.view_audit_log, name='audit-log'),
    path('email/send/', administration.view_send_email, name='send-email'),

    # API
    path('api/health-check/', api.health_check, name='health-check'),

    # Events
    path('events/', event.view_events, name='events'),
    path('events/assign/<int:signup_id>', event.assign_position, name='assign-position'),
    path('events/new/', event.view_new_event, name='new-event'),
    path('events/delete/<int:event_id>', event.delete_event, name='delete-event'),
    path('events/edit/<int:event_id>', event.edit_event, name='edit-event'),
    path('events/archived/', event.view_archived_events, name='archived-events'),
    path('events/<int:event_id>', event.view_event_details, name='event-details'),
    path('events/<int:event_id>/delete-position/<int:position_id>',
         event.delete_position, name='delete-position'),
    path('events/<int:event_id>/signup/<int:pos_id>', event.request_position, name='event-signup'),

    # Feedback
    path('feedback/', feedback.new_feedback, name='feedback'),
    path('feedback/manage/', feedback.manage_feedback, name='manage-feedback'),
    path('feedback/post/<int:feedback_id>', feedback.post_feedback, name='post-feedback'),
    path('feedback/reject/<int:feedback_id>', feedback.reject_feedback, name='reject-feedback'),
    path('feedback/submit/', feedback.submit_feedback, name='submit-feedback'),

    # News
    path('news/', news.view_news, name='news'),
    path('news/article/<int:article_id>', news.view_article, name='article'),
    path('news/article/<int:article_id>/delete', news.delete_article, name='delete-article'),
    path('news/article/new', news.view_submit_new_article, name='new-article'),

    # Pilots
    path('pilot-briefing/', pilots.view_pilot_briefing, name='briefing'),
    path('routes/', pilots.view_preferred_routes, name='routes'),
    path('request-event-staffing/', pilots.view_staffing_request,
         name='request-event-staffing'),

    # Resources
    path('files/', resources.view_files, name='files'),
    path('files/add/', resources.add_file, name='add-file'),
    path('files/delete/<str:file_cat>/<str:file_name>', resources.delete_file, name='delete-file'),

    # SSO (Auth)
    path('login-start/', sso.login_start, name='login-start'),
    path('login/', sso.login, name='login'),
    path('logout/', sso.logout, name='logout'),

    # Training
    path('training/', training.view_training_hub, name='training'),
    path('training/ticket/<int:ticket_id>', training.view_ticket_details, name='ticket-details'),
    path('training/ticket/submit/', training.submit_training_ticket, name='submit-training-ticket'),

    # User
    path('mavp/', user.view_mavp, name='mavp'),
    path('mavp/remove/<str:facility>', user.view_remove_mavp, name='remove-mavp'),
    path('profile/<int:cid>', user.view_profile, name='profile'),
    path('profile/edit/<int:cid>', user.edit_profile, name='edit-profile'),
    path('profile/edit-endorsements/<int:cid>', user.edit_endorsements, name='edit-endorsements'),
    path('roster/', user.view_roster, name='roster'),
    path('staff/', user.view_staff, name='staff'),
    path('statistics/', user.view_statistics, name='statistics'),
    path('visit-request/', user.view_visit_request, name='visit-request'),
    path('visit-request/approve/<int:cid>', user.approve_visit_request, name='approve-visit-request'),
    path('visit-request/deny/<int:cid>', user.deny_visit_request, name='deny-visit-request'),
    path('visit-request/manage/', user.manage_visit_requests, name='manage-visit-requests'),
    path('visit-request/manual-add/', user.manual_add_visitor, name='manual-add-visitor')
]

handler400 = 'apps.views.views.error_400'
handler403 = 'apps.views.views.error_403'
handler404 = 'apps.views.views.error_404'
handler500 = 'apps.views.views.error_500'
