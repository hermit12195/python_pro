import logging
from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils import timezone
from .validators import validate_phone_number

logging.basicConfig(level=logging.DEBUG, filename="app_logs.txt")


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser to include additional fields
    for phone number, address, and custom permissions and groups.

    Attributes:
        phone_number (str): The user's phone number, unique.
        address (str): The user's address.
        groups (ManyToManyField): The groups to which the user belongs.
        user_permissions (ManyToManyField): The permissions granted to the user.

    Methods:
        ads_list(): Returns a list of titles for the user's ads.
        __str__(): Returns the username of the user.
    """
    phone_number = models.CharField(max_length=15, unique=True, validators=[validate_phone_number])
    address = models.CharField(max_length=100)
    groups = models.ManyToManyField("auth.Group", related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custompermission_set", blank=True)

    def ads_list(self):
        """
        Returns a list of titles of the ads created by the user.

        Returns:
            list: A list of strings representing the titles of the user's ads.
        """
        try:
            res = [ad.title for ad in self.ads.all()]
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Ads list is successfully collected!")
            return res
        except AttributeError as e:
            logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")


class Category(models.Model):
    """
    Represents an ad category with a name and description.

    Attributes:
        name (str): The name of the category.
        description (str): A brief description of the category.

    Methods:
        active_ads(): Returns the count of active ads in the category.
        __str__(): Returns the name of the category.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(default="No description yet!", blank=True, null=True)

    def active_ads(self):
        """
        Returns the count of active ads in the category.

        Returns:
            int: The number of active ads in the category.
        """
        try:
            res = self.ads.filter(is_active=True).count()
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Active ads are successfully returned!")
            return res
        except AttributeError as e:
            logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")

    def __str__(self):
        return self.name


class Ad(models.Model):
    """
    Represents an advertisement with details such as title, description, price, and timestamps.

    Attributes:
        title (str): The title of the ad.
        description (str): The description of the ad.
        price (Decimal): The price of the item or service being advertised.
        created_at (datetime): The timestamp when the ad was created.
        updated_at (datetime): The timestamp when the ad was last updated.
        is_active (bool): Whether the ad is active or not.
        user (ForeignKey): The user who created the ad.
        category (ManyToManyField): The categories associated with the ad.

    Methods:
        short_description(): Returns the first 50 characters of the ad's description.
        comments_number(): Returns the number of comments on the ad.
    """
    title = models.CharField(max_length=50)
    description = models.TextField(default="No description yet!", blank=True, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="ads")
    category = models.ManyToManyField(Category, related_name="ads")

    def short_description(self):
        """
        Returns a short version of the ad's description, limited to the first 50 characters.

        Returns:
            str: The first 50 characters of the description, followed by ellipsis.
        """
        try:
            res = f"{self.description[:50]}..."
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Short description is successfully returned!")
            return res
        except AttributeError as e:
            logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")

    def comments_number(self):
        """
        Returns the number of comments associated with the ad.

        Returns:
            int: The number of comments on the ad.
        """
        try:
            res = self.comments.count()
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Comments number is successfully returned!!")
            return res
        except AttributeError as e:
            logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")

    def __str__(self):
        return self.title



class Comment(models.Model):
    """
    Represents a comment on an ad, associated with a user.

    Attributes:
        content (str): The content of the comment.
        created_at (datetime): The timestamp when the comment was created.
        ad (ManyToManyField): The ad that the comment is associated with.
        user (ManyToManyField): The user who made the comment.

    Methods:
        __str__(): Returns the first 50 characters of the comment content.
    """
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ManyToManyField(Ad, related_name="comments")
    user = models.ManyToManyField(User, related_name="comments")

    def __str__(self):
        """
        Returns the first 50 characters of the comment content.

        Returns:
            str: The first 50 characters of the comment content.
        """
        return self.content[:50]


def remove_old_ads():
    """
    Removes ads that are older than 30 days by marking them as inactive.

    This function queries ads that were created more than 30 days ago and sets
    their `is_active` field to False.
    """
    try:
        ads=Ad.objects.filter(created_at__lt=timezone.now() - timedelta(days=30))
        inactive_ads=ads.update(is_active=False)
        logging.info(f"{datetime.utcnow().replace(microsecond=0)} - {inactive_ads} - Old ads are successfully removed!")
    except AttributeError as e:
        logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")
