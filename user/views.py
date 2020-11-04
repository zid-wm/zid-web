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

def view_staff(request):
    atm = User.objects.filter(staff_role='ATM', main_role='HC').first()
    datm = User.objects.filter(staff_role='DATM', main_role='HC').first()
    ta = User.objects.filter(staff_role='TA', main_role='HC').first()
    ec = User.objects.filter(staff_role='EC', main_role='HC').first()
    fe = User.objects.filter(staff_role='FE', main_role='HC').first()
    wm = User.objects.filter(staff_role='WM', main_role='HC').first()

    return render(request, 'staff.html', {
        'page_title': 'Staff',
        'atm': atm,
        'datm': datm,
        'ta': ta,
        'ec': ec,
        'fe': fe,
        'wm': wm
    })