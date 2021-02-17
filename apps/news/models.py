from django.db import models
from apps.user.models import User


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    date_posted = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User, models.SET_NULL, related_name='author', null=True)
