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
    """
    Model representing a task associated with a user.

    This model defines a task with a title, description, due date, and the user to whom the task belongs.

    Attributes:
        title (str): The title of the task. It must be unique and cannot be longer than 100 characters.
        description (str): A detailed description of the task. It cannot be empty.
        due_date (date): The due date for the task. It must be a valid date.
        user (CustomUser): A foreign key reference to the user who owns the task. The task is related to one user.
    """

    title: str = models.CharField(max_length=100, unique=True)
    description: str = models.TextField(null=False, blank=False)
    due_date: models.DateField = models.DateField()
    user: CustomUser = models.ForeignKey(CustomUser, related_name="tasks", on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns a string representation of the task, which is the task's title.

        Returns:
            str: The title of the task.
        """
        return self.title
        