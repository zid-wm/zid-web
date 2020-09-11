from django.db import models


class Roster(models.Model):
    fname = models.TextField()
    lname = models.TextField()
    initials = models.TextField(null=True)
    email = models.TextField(null=True)
    activated = models.IntegerField(default=1)
    rating_id = models.IntegerField()
    can_train = models.IntegerField(default=1)
    can_events = models.IntegerField(default=1)
    visitor = models.IntegerField()
    visitor_from = models.TextField(null=True)
    api_exempt = models.IntegerField(default=0)
    status = models.IntegerField()
    loa = models.IntegerField()

    # Controller Ratings
    # 0 = Not certified
    # 1 = Solo certified
    # 2 = Minor certified
    # 3 = Major certified
    delivery = models.IntegerField(default=0)
    ground = models.IntegerField(default=0)
    tower = models.IntegerField(default=0)
    approach = models.IntegerField(default=0)
    center = models.IntegerField(default=0)

    train_pwr = models.IntegerField(null=True)
    monitor_pwr = models.IntegerField(null=True)
    opt = models.IntegerField(null=True)
    remember_token = models.TextField(null=True)
    json_token = models.CharField(max_length=2000, null=True)
    added_to_facility = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
