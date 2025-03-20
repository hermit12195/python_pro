"""Models Module"""
from django.db import models
from board.models import User


class UserProfile(models.Model):
    """
    A model representing a user's profile, including a one-to-one relationship
    with the User model, a bio, birth date, location, and avatar image.

    Attributes:
        user (OneToOneField): The user associated with this profile.
        bio (TextField): A short biography of the user, with a default value.
        birth_date (DateField): The user's birth date.
        location (CharField): The user's location, with a default value.
        avatar (FileField): The user's avatar image, with a default placeholder image.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, default="No bio yet!")
    birth_date = models.DateField(null=True)
    location = models.CharField(max_length=100, default="No location yet!")
    avatar = models.FileField(upload_to="avatar_storage/", default='default.jpg', blank=True)

    def __str__(self) -> str:
        """
        Returns the username associated with the user profile.

        Returns:
            str: The user's username.
        """
        return self.user.username


