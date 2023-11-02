import requests
import os

from apscheduler.schedulers.background import BackgroundScheduler
from .models import User
from apps.administration.models import ActionLog, MAVP
from django.utils import timezone


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_roster, 'interval', minutes=30)
    scheduler.add_job(update_loa, 'cron', hour=0)
    scheduler.start()


def update_roster():
    #############################################
    # Update home controllers
    #############################################
    roster = requests.get(
        f'{os.getenv("VATUSA_API_URL")}/facility/ZID/roster/both',
        params={
            'apikey': os.getenv('API_KEY')
        }
    ).json()['data']

    for user in roster:
        if not User.objects.filter(cid=user['cid']).exists():
            new_user = User(
                first_name=user['fname'].capitalize(),
                last_name=user['lname'].capitalize(),
                cid=int(user['cid']),
                email=user['email'],
                oper_init=assign_operating_initials(
                    user['fname'][0], user['lname'][0]
                ),
                rating=user['rating_short'],
                home_facility=user['facility'],
                main_role='HC' if user['facility'] == 'ZID' else 'VC'
            )

            if user['rating_short'] in ['I1', 'I3'] and user['facility'] == 'ZID':
                new_user.training_role = 'INS'
            for role in user['roles']:
                if role['facility'] == 'ZID':
                    if role['role'] in ['INS', 'MTR']:
                        new_user.training_role = role['role']
                    else:
                        new_user.staff_role = role['role']
            new_user.save()
            new_user.assign_initial_certs()

            ActionLog(
                action=f'New home/visiting controller {new_user.full_name} was created by system.'
            ).save()

        else:
            edit_user = User.objects.get(cid=user['cid'])

            edit_user.rating = user['rating_short']
            edit_user.home_facility = user['facility']
            edit_user.email = user['email']
            edit_user.main_role = 'HC' if user['facility'] == 'ZID' else 'VC'

            # Keep track of whether training/staff roles are present,
            # else remove the appropriate tags from current user.
            training_role = False
            staff_role = False

            if user['rating_short'] in ['I1', 'I3'] and user['facility'] == 'ZID':
                edit_user.training_role = 'INS'
                training_role = True
            for role in user['roles']:
                if role['facility'] == 'ZID':
                    if role['role'] == 'INS' or role['role'] == 'MTR':
                        edit_user.training_role = role['role']
                        training_role = True
                    else:
                        edit_user.staff_role = role['role']
                        staff_role = True

            if not training_role:
                edit_user.training_role = None
            if not staff_role:
                edit_user.staff_role = None

            # If user is rejoining the ARTCC after being marked as inactive
            if edit_user.status == 2:
                edit_user.status = 0
                edit_user.email = user['email']
                edit_user.oper_init = assign_operating_initials(
                    user['fname'][0], user['lname'][0], edit_user)
                edit_user.main_role = 'HC' if user['facility'] == 'ZID' else 'VC'

                edit_user.save()
                ActionLog(
                    action=f'Home/visiting controller {edit_user.full_name} was marked active by system.'
                ).save()
            edit_user.save()
            edit_user.assign_initial_certs()

    #############################################
    # Set controllers to inactive if they are no longer on VATUSA roster
    #############################################
    roster_cids = [user['cid'] for user in roster]
    for user in User.objects.filter(main_role__in=['HC', 'VC']).exclude(status=2):
        if user.cid not in roster_cids:
            user.status = 2
            user.save()
            ActionLog(
                action=f'Home/visiting controller {user.full_name} was set as inactive by system.'
            ).save()

    #############################################
    # Update MAVP controllers
    #############################################
    for mavp_artcc in MAVP.objects.all():
        mavp_roster = requests.get(
            f'{os.getenv("VATUSA_API_URL")}/facility/{mavp_artcc.facility_short}/roster',
            params={
                'apikey': os.getenv('API_KEY')
            }
        ).json()['data']

        for user in mavp_roster:
            if user['rating'] > 1:
                if not User.objects.filter(cid=user['cid']).exists():
                    new_user = User(
                        first_name=user['fname'].capitalize(),
                        last_name=user['lname'].capitalize(),
                        cid=int(user['cid']),
                        email=user['email'],
                        oper_init=assign_operating_initials(
                            user['fname'][0], user['lname'][0]
                        ),
                        rating=user['rating_short'],
                        main_role='MC',
                        home_facility=mavp_artcc.facility_short
                    )
                    new_user.save()
                    new_user.assign_initial_certs()
                    ActionLog(
                        action=f'New MAVP controller {new_user.full_name} was created by system.'
                    ).save()

                # Don't update full visiting controllers during the MAVP update
                elif User.objects.get(cid=user['cid']).main_role == 'MC':
                    edit_user = User.objects.get(cid=user['cid'])
                    edit_user.rating = user['rating_short']
                    edit_user.home_facility = mavp_artcc.facility_short

                    if edit_user.status == 2:
                        edit_user.status = 0
                        edit_user.email = user['email']
                        edit_user.oper_init = assign_operating_initials(
                            user['fname'][0], user['lname'][0], edit_user)
                        edit_user.main_role = 'MC'

                        edit_user.save()
                        edit_user.assign_initial_certs()
                        ActionLog(
                            action=f'MAVP Controller {edit_user.full_name} was marked active by system.'
                        ).save()
                    edit_user.save()

        # Set MAVP controllers inactive
        mavp_roster_cids = [user['cid'] for user in mavp_roster]
        for user in User.objects.filter(main_role='MC').exclude(status=2):
            if user.cid not in mavp_roster_cids:
                user.status = 2
                user.save()
                ActionLog(
                    action=f'MAVP Controller {user.full_name} was set as inactive by system.'
                ).save()


def gcap_certification_update_check(user: User):
    """Temporary function to transfer all user certifications to the new GCAP-compliant
    system. Should be removed with the next website update."""
    if user.del_cert < 100:
        if user.del_cert == 2:
            user.del_cert = 102
        else:
            user.del_cert = 100

    if user.gnd_cert < 100:
        if user.gnd_cert == 2:
            user.gnd_cert = 102
        elif user.gnd_cert == 1:
            user.gnd_cert = 101
        else:
            user.gnd_cert = 100

    if user.twr_cert < 100:
        if user.twr_cert == 2:
            user.twr_cert = 102
        elif user.twr_cert == 1 or user.twr_cert == 3:
            user.twr_cert = 101
        else:
            user.twr_cert = 100

    if user.app_cert < 100:
        if user.app_cert == 2:
            user.app_cert = 102
        elif user.app_cert == 1 or user.app_cert == 3:
            user.app_cert = 101
        else:
            user.app_cert = 100

    if user.ctr_cert < 100:
        if user.ctr_cert == 2:
            user.ctr_cert = 102
        else:
            user.ctr_cert = 100

    user.save()


def update_loa():
    for user in User.objects.filter(status=1):
        if user.loa_until is None or user.loa_until <= timezone.now().date():
            user.status = 0
            user.loa_last_month = True
            ActionLog(
                action=f'The leave of absence for {user.full_name} expired; marked active by system.'
            ).save()


# Major credit to ZHU ARTCC (and Mike Romashov) for these two algorithms.
def base26decode(str_n):
    int_n = 0
    for pos, char in enumerate(str_n):
        int_n += (ord(char) - 65) * (26 ** (len(str_n) - pos - 1))
    return int_n


def base26encode(int_n):
    str_n = ''
    while int_n > 25:
        q, r = divmod(int_n, 26)
        str_n = chr(r + 65) + str_n
        int_n = q
    str_n = chr(int_n + 65) + str_n
    return str_n


def assign_operating_initials(f_init, l_init, user=None):
    oi = (f_init + l_init).upper()
    while User.objects.filter(oper_init=oi).exclude(cid=user.cid if user else 0).exists():
        new_oi = base26decode(oi) + 1
        oi = base26encode(new_oi if new_oi <= 675 else 0)
    if len(oi) < 2:
        oi = 'A' + oi
    return oi


def add_visitor(cid):
    response = requests.post(
        f'{os.getenv("VATUSA_API_URL")}/facility/ZID/roster/manageVisitor/{cid}',
        params={'apikey': os.getenv('API_KEY')}
    ).json()

    if response['status'] == 'OK':
        print(f'Added CID {cid} to visiting roster.')
    else:
        print(f'Error adding CID {cid} to visiting roster: {response}')

    if User.objects.filter(
        cid=cid,
        main_role='MC'
    ).exists():
        User.objects.get(cid=cid).delete()
