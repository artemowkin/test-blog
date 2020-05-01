from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
