from typing import Any

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from channels.layers import get_channel_layer

from blog.models import Post, Comment
from chats.ws.constants import STAFF_GROUP_NAME


@receiver(post_save, sender=Post)
def signup_email(sender: Any, instance: Post, created: bool, **kwargs: Any) -> None:
    """
    Sends a notification email to the post creator after a new Post instance is created.

    Args:
        sender (Any): The sender of the signal (Post model).
        instance (Post): The Post instance that was saved.
        created (bool): A boolean indicating if the instance is newly created.
        **kwargs (Any): Additional keyword arguments passed by the signal.
    """
    if created:
        subject = 'The Post Created!'
        message = f'{instance.user.username}! You have successfully submitted new post!'
        recipient_list = [instance.user.email]

        send_mail(
            subject,
            message,
            'admin@blog.com',
            recipient_list,
            fail_silently=False,
        )


@receiver(post_save, sender=Comment)
def signup_email(sender: Any, instance: Comment, created: bool, **kwargs: Any) -> None:
    """
    Sends a notification email to the post creator when a new comment is made on their post.

    Args:
        sender (Any): The sender of the signal (Comment model).
        instance (Comment): The Comment instance that was saved.
        created (bool): A boolean indicating if the instance is newly created.
        **kwargs (Any): Additional keyword arguments passed by the signal.
    """
    if created:
        subject = 'New comment!'
        message = f'{instance.post.user.username}! Somebody has commented your post!'
        recipient_list = [instance.post.user.email]

        send_mail(
            subject,
            message,
            'admin@blog.com',
            recipient_list,
            fail_silently=False,
        )

@receiver(post_save, sender=Post)
def group_message(sender: Any, instance: Post, created: bool, **kwargs: Any):
    if created:
        channel_layer=get_channel_layer()
        print(f"Sending group message: 'The new Post was created'")
        async_to_sync(channel_layer.group_send)(STAFF_GROUP_NAME, {"type": "group_message", "group_message": "The new Post was created"})

