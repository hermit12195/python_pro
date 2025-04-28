from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from taggit.managers import TaggableManager
from typing import Optional


def user_photo_path(instance: 'Profile', filename: str) -> str:
    """
    Generates the path for user photos based on the user's ID.

    Args:
        instance (Profile): The Profile instance.
        filename (str): The name of the file being uploaded.

    Returns:
        str: The path where the photo will be stored.
    """
    return f'user_{instance.user.id}/{filename}'


class BlogUser(AbstractUser):
    """
    A custom user model that extends AbstractUser to include email as a unique field.

    Attributes:
        email (str): The user's email address.
    """
    email: str = models.EmailField(unique=True, validators=[EmailValidator])


class Profile(models.Model):
    """
    Profile model for the BlogUser, containing personal information and photo.

    Attributes:
        user (BlogUser): The related BlogUser instance.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        bio (str): The user's biography.
        birth_date (date): The user's birth date.
        photo (ImageField): The user's profile photo.
    """
    user: models.OneToOneField = models.OneToOneField(BlogUser, on_delete=models.CASCADE, related_name="profile",
                                                      null=True)
    first_name: Optional[str] = models.CharField(max_length=50, null=True)
    last_name: Optional[str] = models.CharField(max_length=50, null=True)
    bio: str = models.TextField(default="No bio yet!")
    birth_date: models.DateField = models.DateField()
    photo: models.ImageField = models.ImageField(upload_to=user_photo_path, default='default.png', blank=True)

    def __str__(self) -> str:
        """
        String representation of the Profile object.

        Returns:
            str: The bio of the user.
        """
        return self.bio


class Category(models.Model):
    """
    Category model for grouping posts.

    Attributes:
        title (str): The title of the category.
        description (str): A description of the category.
    """
    title: str = models.CharField(max_length=50)
    description: Optional[str] = models.TextField(default="No description yet!", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def active_posts(self) -> int:
        """
        Returns the count of active posts in the category.

        Returns:
            int: The number of active posts in the category.
        """
        return self.posts.filter(is_active=True).count()

    def __str__(self) -> str:
        """
        String representation of the Category object.

        Returns:
            str: The title of the category.
        """
        return self.title


class Comment(models.Model):
    """
    Comment model for user comments on posts.

    Attributes:
        plot (str): The content of the comment.
        user (BlogUser): The user who made the comment.
        post (Post): The post the comment is related to.
        created_datetime (datetime): The timestamp of when the comment was created.
    """
    plot: str = models.TextField(null=False, blank=False)
    user: models.ForeignKey = models.ForeignKey(BlogUser, on_delete=models.DO_NOTHING, related_name="comments")
    post: Optional[models.ForeignKey] = models.ForeignKey('Post', on_delete=models.DO_NOTHING, related_name="comments",
                                                          null=True)
    created_datetime: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        String representation of the Comment object, showing the first 10 characters of the plot.

        Returns:
            str: The truncated content of the comment.
        """
        return f"{self.plot[:10]}..."


class Post(models.Model):
    """
    Post model for creating and managing blog posts.

    Attributes:
        title (str): The title of the post.
        plot (str): The content of the post.
        tag (TaggableManager): Tags associated with the post.
        user (BlogUser): The user who created the post.
        category (ManyToManyField): Categories associated with the post.
        is_active (bool): Indicates if the post is active or not.
        created_datetime (datetime): The timestamp when the post was created.
        modified_datetime (datetime): The timestamp when the post was last modified.
    """
    title: str = models.CharField(max_length=50)
    plot: str = models.TextField(null=False, blank=False)
    tag: TaggableManager = TaggableManager()
    user: models.ForeignKey = models.ForeignKey(BlogUser, on_delete=models.DO_NOTHING, related_name="posts")
    category: models.ManyToManyField = models.ManyToManyField(Category, related_name="posts")
    is_active: bool = models.BooleanField(default=True)
    created_datetime: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    modified_datetime: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        String representation of the Post object, showing the first 10 characters of the title.

        Returns:
            str: The truncated title of the post.
        """
        return f"{self.title[:10]}..."
