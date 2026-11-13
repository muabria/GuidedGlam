from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Django's built-in user (username, hashed password, is_staff, ...)
    with one change: email is required to be unique.

    `is_staff` plays the role of `isAdmin` in the old Express code.
    """

    email = models.EmailField(unique=True)
