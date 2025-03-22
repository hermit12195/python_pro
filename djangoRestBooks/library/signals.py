"""Signals Module"""
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_signal(sender, instance, created=False, **kwargs):
    """
    Signal handler to create an authentication token when a new User is created.

    This function is triggered whenever a new User instance is saved. If the User is newly created,
    an authentication token is created and associated with that user.

    Args:
        sender (Any): The sender of the signal, in this case, the User model.
        instance (User): The instance of the User model that was just saved.
        created (bool): A flag indicating whether the instance is newly created. Defaults to False.
        **kwargs (Any): Additional keyword arguments passed by the signal.

    Returns:
        None
    """
    if created:
        Token.objects.create(user=instance)
