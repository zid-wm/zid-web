import requests

from django.shortcuts import render

from .forms import RoutesForm, StaffingForm


def view_pilot_briefing(request):
    return render(request, 'briefing.html', {
        'page_title': 'Pilot Briefing'
    })


def view_preferred_routes(request):
    routes = None
    if request.method == 'POST':
        form = RoutesForm(request.POST)
        routes = requests.get(
            'https://api.aviationapi.com/v1/preferred-routes/search',
            params={
                'origin': request.POST['dep_apt'],
                'dest': request.POST['arr_apt']
            }
        ).json()
    else:
        form = RoutesForm()

    return render(request, 'routes.html', {
        'page_title': 'IFR Routes',
        'form': form,
        'routes': routes
    })


def view_staffing_request(request):
    if request.method == 'POST':
        form = StaffingForm(request.POST)
    else:
        form = StaffingForm()

    return render(request, 'request-event-staffing.html', {
        'page_title': 'Request Staffing',
        'form': form
    })
