"""DRF Filters Module"""
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    Filter set for the Book model to filter books by various fields.

    This class allows filtering of books based on their title, author, genre, and publication year.
    The filters support case-insensitive searches for title, author, and genre, and exact matches for publication year.

    Attributes:
        title (django_filters.CharFilter): Filters books by title using 'icontains' (case-insensitive contains).
        author (django_filters.CharFilter): Filters books by author using 'iexact' (case-insensitive exact match).
        genre (django_filters.CharFilter): Filters books by genre using 'iexact' (case-insensitive exact match).
        publication_year (django_filters.NumberFilter): Filters books by publication year using 'iexact' (exact match).
    """

    title: django_filters.CharFilter = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    author: django_filters.CharFilter = django_filters.CharFilter(field_name="author", lookup_expr="iexact")
    genre: django_filters.CharFilter = django_filters.CharFilter(field_name="genre", lookup_expr="iexact")
    publication_year: django_filters.NumberFilter = django_filters.NumberFilter(field_name="publication_year",
                                                                                lookup_expr="iexact")

    class Meta:
        """
        Meta configuration for the filter set.

        - model: Book - The model to filter on.
        - fields: List of fields to include in the filtering. It includes author, genre, and publication_year.
        """
        model = Book
        fields = ["author", "genre", "publication_year"]
