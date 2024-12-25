from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
