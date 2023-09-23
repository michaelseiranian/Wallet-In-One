"""Models in the accounts app"""

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import ArrayField
# Create your models here.

class User(AbstractUser):
    """User model used for authentication."""

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(
            #regex=r'^@\w{3,}$',
            regex=r'^(?=.*[a-zA-Z]{4,}).*$',
            message='Username must contain at least 4 alphabetical characters'
        )]
    )
    first_name = models.CharField(
        max_length=15,
        blank=False
    )
    last_name = models.CharField(
        max_length=15,
        blank=False
    )
    email = models.EmailField(
        unique=True,
        max_length=25,
        blank=False
    )

    
