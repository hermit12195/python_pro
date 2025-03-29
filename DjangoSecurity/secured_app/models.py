from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending the base Django AbstractUser.

    Adds a unique email field with email validation to ensure each user has a unique and valid email address.

    Attributes:
        email (EmailField): The email address of the user, which must be unique and validated.
    """

    email: str = models.EmailField(unique=True, validators=[EmailValidator])


class Task(models.Model):
    title=models.CharField(max_length=100, unique=True)
    description=models.TextField(null=False, blank=False)
    due_date=models.DateField()
    user=models.ForeignKey(CustomUser, related_name="tasks", on_delete=models.DO_NOTHING)



