from django.db.models.signals import post_save
from django.dispatch import receiver

from conduit.apps.profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # we check for created as we wanna do this only upon creation and
    # not if it is already created and just being updated.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)