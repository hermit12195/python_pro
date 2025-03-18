"""Module for Django signals"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ad, remove_old_ads
from django.core.mail import send_mail


@receiver(post_save, sender=Ad)
def remove_handler(sender, **kwargs):
    """
    Signal handler that triggers the removal of old ads.

    This function is executed after an Ad instance is saved. It calls the
    `remove_old_ads` function to deactivate ads older than 30 days.

    Args:
        sender (Model): The model class that triggered the signal.
        **kwargs: Additional keyword arguments.
    """
    remove_old_ads()


@receiver(pre_save, sender=Ad)
def price_validator(sender, instance, **kwargs):
    """
    Signal handler that validates the price of an Ad before saving.

    This function ensures that the price of an Ad instance is not negative.
    If the price is negative, it raises a `ValueError`.

    Args:
        sender (Model): The model class that triggered the signal.
        instance (Ad): The Ad instance being saved.
        **kwargs: Additional keyword arguments.

    Raises:
        ValueError: If the price of the ad is negative.
    """
    if instance.price < 0:
        raise ValueError("The price may not be negative!")


@receiver(post_save, sender=Ad)
def send_email_on_ad_creation(sender, instance, created, **kwargs):
    """
    Signal handler that sends an email notification when a new Ad is created.

    This function is executed after an Ad instance is successfully saved.
    If the ad is newly created, it sends an email notification to a predefined
    recipient list.

    Args:
        sender (Model): The model class that triggered the signal.
        instance (Ad): The Ad instance that was saved.
        created (bool): Indicates whether the instance was newly created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        subject = 'New Ad is created!'
        message = f'Congrats! New ad "{instance.title}" was created!'
        recipient_list = [instance.user.email]

        send_mail(
            subject,
            message,
            'vladyslav12195@gmail.com',
            recipient_list,
            fail_silently=False,
        )
