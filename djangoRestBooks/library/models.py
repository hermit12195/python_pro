"""Django Models module"""
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    A model representing a book in the library.

    This model holds the details of a book including its title, author, genre, publication year, and creation date.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        genre (str): The genre of the book.
        publication_year (int): The year the book was published.
        created_at (datetime): The timestamp of when the book entry was created.

    Methods:
        __str__(): Returns a string representation of the book (the title).
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="books", null=True)

    def __str__(self):
        return self.title
