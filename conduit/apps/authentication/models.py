import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from conduit.apps.core.models import TimestampedModel

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

    # Overriding the function from BaseUserManager. A function to make a superuser
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    # indexing username and email for faster lookup
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # defining what to use for login to Django
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # should be managed by
    objects = UserManager()

    def __str__(self):
        return self.email

    # setting a dynamic property for the user's jwt token
    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # generating a JWT storing user ID and expiry of 60 days into the future
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')