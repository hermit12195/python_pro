"""Views Module"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer
from .models import Book
from .filters import BookFilter
from .paginations import BookPagination
from .permissions import BookPermission


class BookView(ModelViewSet):
    """
    Viewset for handling CRUD operations on the Book model.

    This viewset allows retrieving, creating, updating, and deleting books.
    It supports filtering, sorting, and pagination.

    Attributes:
        queryset (Type[Book]): The queryset of all books.
        serializer_class (Type[BookSerializer]): The serializer class for serializing book data.
        permission_classes (list): A list of permission classes to apply on the view.
        filter_backends (tuple): The filter backends to use for filtering the book list.
        filterset_class (Type[BookFilter]): The filter class for filtering the book list.
        pagination_class (Type[BookPagination]): The pagination class to paginate the book list.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    pagination_class = BookPagination

    def get_queryset(self):
        """
        Returns the queryset of books, optionally sorted based on a query parameter.

        This method checks for a 'sort' query parameter and sorts the books based on
        the provided field. If no 'sort' parameter is provided, it returns all books without sorting.

        Args:
            None

        Returns:
            Type[Book]: The queryset of books, sorted if 'sort' parameter is provided.
        """
        sort_by = self.request.query_params.get('sort', '')
        if sort_by:
            return Book.objects.all().order_by(sort_by)
        return Book.objects.all()

    def perform_create(self, serializer):
        """
        Saves the book instance, associating it with the current user.

        This method overrides the default perform_create to ensure the book
        is created with the currently authenticated user.

        Args:
            serializer (BookSerializer): The serializer instance containing the data to save.

        Returns:
            None
        """
        serializer.save(user=self.request.user)


class BookDetails(RetrieveUpdateDestroyAPIView):
    """
    View for handling the retrieval, updating, and deletion of a single book.

    This view allows performing CRUD operations on a single book instance.

    Attributes:
        queryset (Type[Book]): The queryset of all books.
        serializer_class (Type[BookSerializer]): The serializer class for serializing book data.
        permission_classes (list): A list of permission classes to apply on the view.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermission]
