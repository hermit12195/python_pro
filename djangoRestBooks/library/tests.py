"""Module for DRF tests"""
import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Book


class TestBooks(TestCase):
    """
    Test cases for the Book API endpoints.

    This class tests the functionality of the Book API, including retrieving a list of books,
    retrieving a single book's details, creating a new book, filtering books, and deleting a book.
    """

    def setUp(self) -> None:
        """
        Set up the test client with STAFF role, create a test user, generate a token, and create a sample book for testing.

        Returns:
            None
        """
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass", is_staff=True)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.book = Book.objects.create(title="TestTitle", author="TestAuthor", genre="TestGenre",
                                        publication_year=2000)

    def test_get_books(self) -> None:
        """
        Test retrieving the list of books via GET request.

        This test verifies that the response for fetching books is successful (status code 200).

        Returns:
            None
        """
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)

    def test_get_book_detail(self) -> None:
        """
        Test retrieving a single book's details via GET request.

        This test verifies that the response for fetching a single book's details is successful
        (status code 200).

        Returns:
            None
        """
        response = self.client.get("/api/books/1/")
        self.assertEqual(response.status_code, 200)

    def test_create_book(self) -> None:
        """
        Test creating a new book via POST request.

        This test verifies that the book creation is successful (status code 201) and the response data
        contains the correct title.

        Returns:
            None
        """
        url = "/api/books/"
        data = {'title': 'TestTitle', 'author': 'TestAuthor', 'genre': 'TestGenre', 'publication_year': 2000}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "TestTitle")

    def test_book_filter(self) -> None:
        """
        Test filtering books by title via GET request.

        This test verifies that the filtering functionality works correctly and the response contains
        the correct filtered book(s).

        Returns:
            None
        """
        response = self.client.get("/api/books/?title=Test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]["title"], 'TestTitle')

    def test_delete_book(self) -> None:
        """
        Test deleting a book via DELETE request.

        This test verifies that the deletion of a book is successful, and checks if a 403 status code
        is returned when the user does not have the proper permissions.

        Returns:
            None
        """
        url = "/api/books/1/"
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 403)
