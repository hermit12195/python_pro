from celery import shared_task
from django.core.mail import send_mail

from blog.models import BlogUser


@shared_task
def signup_email(user_id) -> None:
    """
    Sends a welcome email to a user with the given ID.

    Args:
        user_id (int): The ID of the BlogUser to whom the welcome email will be sent.
    """
    instance = BlogUser.objects.get(id=user_id)
    subject = 'Welcome to the Blog!!!'
    message = f'{instance.username}! Thanks for the signup!'
    recipient_list = [instance.email]

    send_mail(
        subject,
        message,
        'admin@blog.com',
        recipient_list,
        fail_silently=False,
    )


@shared_task
def adv_email(user_id) -> None:
    """
    Sends an advertisement email to a user with the given ID.

    Args:
        user_id (int): The ID of the BlogUser to whom the advertisement will be sent.
    """
    instance = BlogUser.objects.get(id=user_id)
    subject = 'Ugly Advertisement!!!'
    message = f'{instance.username}! Here is the list of adds we offer!'
    recipient_list = [instance.email]

    send_mail(
        subject,
        message,
        'admin@blog.com',
        recipient_list,
        fail_silently=False,
    )


@shared_task
def user_quantity(*args, **kwargs):
    """
    Appends the current number of BlogUser entries in the database
    to the file 'user_quantity_logs.txt'.

    Args:
        *args: Unused positional arguments.
        **kwargs: Unused keyword arguments.
    """
    with open("user_quantity_logs.txt", "a") as fo:
        fo.write(f"\nThe number of users in DB is:{BlogUser.objects.all().count()}")
        fo.close()
