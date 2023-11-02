from django.db import models


RATING_INTS = {
    'OBS': 0,
    'S1': 1,
    'S2': 2,
    'S3': 3,
    'C1': 4,
    'C3': 5,
    'I1': 6,
    'I3': 7,
    'SUP': 8,
    'ADM': 9
}

ENDORSEMENTS = (
    (0, 'OLD - No Endorsement'),
    (1, 'OLD - Minor Endorsement'),
    (2, 'OLD - Major Endorsement'),
    (3, 'OLD - Solo Endorsement'),
    (100, 'Not Certified'),
    (101, 'Simple/Solo'),
    (102, 'Advanced/Certified')
)


class User(models.Model):
    STATUSES = (
        (0, 'Active'),
        (1, 'LOA'),
        (2, 'Inactive')
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    cid = models.IntegerField(primary_key=True)
    email = models.EmailField(null=True, blank=True)
    oper_init = models.CharField(max_length=16)
    home_facility = models.CharField(max_length=32, null=True, blank=True)
    rating = models.CharField(max_length=32)

    main_role = models.CharField(max_length=32)
    staff_role = models.CharField(max_length=32, null=True, blank=True)
    assistant_staff_role = models.CharField(max_length=32, null=True, blank=True)
    training_role = models.CharField(max_length=32, null=True, blank=True)
    mentor_level = models.CharField(max_length=32, null=True, blank=True)

    del_cert = models.IntegerField(default=100, choices=ENDORSEMENTS)
    gnd_cert = models.IntegerField(default=100, choices=ENDORSEMENTS)
    twr_cert = models.IntegerField(default=100, choices=ENDORSEMENTS)
    app_cert = models.IntegerField(default=100, choices=ENDORSEMENTS)
    ctr_cert = models.IntegerField(default=100, choices=ENDORSEMENTS)
    solo_cert = models.CharField(max_length=32, null=True, blank=True)

    profile_picture = models.URLField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    # TODO Does this need to be a separate (many-to-one) relation?
    staff_comment = models.TextField(null=True, blank=True)
    staff_comment_author = models.ForeignKey(
        'self', models.SET_NULL, null=True, blank=True)

    status = models.IntegerField(default=0, choices=STATUSES)
    loa_until = models.DateField(null=True, blank=True)
    loa_last_month = models.BooleanField(default=False)
    activity_exempt = models.BooleanField(default=False)
    prevent_event_signup = models.BooleanField(default=False)

    # Boolean function to determine whether user is staff
    @property
    def is_staff(self):
        return self.staff_role is not None and self.staff_role != ''

    # Boolean function to determine whether user is senior staff
    # Webmaster is included in list to ensure the ability to reproduce errors and debug
    @property
    def is_senior_staff(self):
        return self.staff_role in ['ATM', 'DATM', 'TA', 'WM']

    # Boolean function to determine whether user is a member of training staff
    @property
    def is_trainer(self):
        return self.training_role is not None and self.training_role != ''

    # Return user's full name
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def rating_int(self):
        return RATING_INTS[self.rating]

    # Assign minor certifications to MAVP controllers
    def assign_initial_certs(self):
        if RATING_INTS[self.rating] > 0:
            self.del_cert = 102
            self.gnd_cert = 102
            if RATING_INTS[self.rating] > 1:
                self.twr_cert = 102
                if RATING_INTS[self.rating] > 2:
                    self.app_cert = 102
        self.save()


class VisitRequest(models.Model):
    REQUEST_STATUSES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Denied')
    )
    cid = models.IntegerField()
    description = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, choices=REQUEST_STATUSES)
