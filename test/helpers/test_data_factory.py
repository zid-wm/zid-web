from django.test import RequestFactory

from apps.user.models import User


def get_request(path: str, **kwargs):
    factory = RequestFactory()
    request = factory.get(path)
    if 'user_kwargs' in kwargs:
        request.user_obj = controller(**kwargs['user_kwargs'])
    else:
        request.user_obj = controller()
    return request


def controller(**kwargs):
    user = User(
        first_name=kwargs['first_name'] if 'first_name' in kwargs else 'FirstName',
        last_name=kwargs['last_name'] if 'last_name' in kwargs else 'LastName',
        cid=kwargs['cid'] if 'cid' in kwargs else 123456,
        email=kwargs['email'] if 'email' in kwargs else 'first.last@mail.com',
        oper_init=kwargs['oper_init'] if 'oper_init' in kwargs else 'FL',
        home_facility=kwargs['home_facility'] if 'home_facility' in kwargs else 'ZID',
        rating=kwargs['rating'] if 'rating' in kwargs else 4,

        main_role=kwargs['main_role'] if 'main_role' in kwargs else 'HC',
        staff_role=kwargs['staff_role'] if 'staff_role' in kwargs else 'ATM',
        assistant_staff_role=
        kwargs['assistant_staff_role'] if 'assistant_staff_role' in kwargs else None,
        training_role=kwargs['training_role'] if 'training_role' in kwargs else None,
        mentor_level=kwargs['mentor_level'] if 'mentor_level' in kwargs else None,

        del_cert=kwargs['del_cert'] if 'del_cert' in kwargs else 2,
        gnd_cert=kwargs['gnd_cert'] if 'gnd_cert' in kwargs else 2,
        twr_cert=kwargs['twr_cert'] if 'twr_cert' in kwargs else 2,
        app_cert=kwargs['app_cert'] if 'app_cert' in kwargs else 2,
        ctr_cert=kwargs['ctr_cert'] if 'ctr_cert' in kwargs else 2,
        solo_cert=kwargs['solo_cert'] if 'solo_cert' in kwargs else None,

        profile_picture=kwargs['profile_picture'] if 'profile_picture' in kwargs else None,
        biography=kwargs['biography'] if 'biography' in kwargs else None,

        staff_comment=kwargs['staff_comment'] if 'staff_comment' in kwargs else None,
        staff_comment_author=
        kwargs['staff_comment_author'] if 'staff_comment_author' in kwargs else None,

        status=kwargs['status'] if 'status' in kwargs else 0,
        loa_until=kwargs['loa_until'] if 'loa_until' in kwargs else None,
        loa_last_month=kwargs['loa_last_month'] if 'loa_last_month' in kwargs else False,
        activity_exempt=kwargs['activity_exempt'] if 'activity_exempt' in kwargs else False,
        prevent_event_signup=
        kwargs['prevent_event_signup'] if 'prevent_event_signup' in kwargs else False
    )
    return user
