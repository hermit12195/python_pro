"""Signals Module"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from board.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender: type, instance: User, created: bool, **kwargs: dict) -> None:
    """
    Signal handler that automatically creates a UserProfile when a new User
    instance is created.

    Args:
        sender (type): The model class that sent the signal (User in this case).
        instance (User): The User instance that was just created.
        created (bool): A flag indicating if the instance was created or updated.
        **kwargs (dict): Additional keyword arguments.

    Returns:
        None
    """
    if created:
        UserProfile.objects.create(user=instance)
