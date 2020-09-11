from django.db import models


class VatsimAtcStats(models.Model):
    cid = models.ForeignKey('Roster', on_delete=models.CASCADE)
    total_time = models.DecimalField(max_digits=8, decimal_places=4)
    s1_time = models.DecimalField(max_digits=8, decimal_places=4)
    s2_time = models.DecimalField(max_digits=8, decimal_places=4)
    s3_time = models.DecimalField(max_digits=8, decimal_places=4)
    c1_time = models.DecimalField(max_digits=8, decimal_places=4)
    c3_time = models.DecimalField(max_digits=8, decimal_places=4)
    i1_time = models.DecimalField(max_digits=8, decimal_places=4)
    i3_time = models.DecimalField(max_digits=8, decimal_places=4)
    sup_time = models.DecimalField(max_digits=8, decimal_places=4)
    adm_time = models.DecimalField(max_digits=8, decimal_places=4)
