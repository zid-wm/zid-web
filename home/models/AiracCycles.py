from django.db import models


class AiracCycles(models.Model):
    airac_cycle = models.TextField()
    effective_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
