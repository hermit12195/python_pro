"""Pagination Module"""
from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    """
    Custom Class for Pagination.
    Lists only 10 objects within a page.
    """
    page_size = 10
