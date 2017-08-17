from django.db import models

from conduit.apps.core.models import TimestampedModel

class Profile(TimestampedModel):
    # Establishing one-to-one relationship between User and Profile
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

