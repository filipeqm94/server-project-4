from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    primary_language = models.CharField(max_length=100, blank=False, null=False)
    learning_language = models.CharField(max_length=100, blank=False, null=False)
