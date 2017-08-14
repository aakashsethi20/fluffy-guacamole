import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):
    """
    This class will handle the creation of our custom user to suit JWT needs.
    """

    # Overriding the create_user() function to suit our own needs
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have an username.')
        
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    # A function to make a super_user
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_superuser(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user