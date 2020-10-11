from django.shortcuts import render
from user.models import User

def view_roster(request):
    home_roster = User.objects.filter(
        main_role='HC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    visit_roster = User.objects.filter(
        main_role='VC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'home_facility',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    mavp_roster = User.objects.filter(
        main_role='MC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'home_facility',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    return render(request, 'roster.html', {
        'page_title': 'Roster',
        'home_roster': home_roster,
        'visit_roster': visit_roster,
        'mavp_roster': mavp_roster
    })