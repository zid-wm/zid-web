from django.db import models


class FaaCharts(models.Model):
    apt_ident = models.TextField()
    alnum = models.TextField()
    chartseq = models.IntegerField()
    chart_code = models.TextField()
    chart_name = models.TextField()
    user_action = models.TextField(null=True)
    pdf_name = models.TextField()
    cn_flg = models.TextField()
    cn_section = models.TextField(null=True)
    cn_page = models.TextField(null=True)
    bv_section = models.TextField(null=True)
    bv_page = models.TextField(null=True)
    procuid = models.TextField(null=True)
    two_colored = models.TextField(null=True)
    civil = models.TextField(null=True)
    faanfd18 = models.TextField(null=True)
    copter = models.TextField(null=True)
    amdtnum = models.TextField(null=True)
    amdtdate = models.TextField(null=True)
