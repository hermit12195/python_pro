"""Permissions Module"""
from rest_framework import permissions


class BookPermission(permissions.BasePermission):
    """
    Custom permission class to manage access control for book-related operations.

    This class grants permissions based on the HTTP method and the user's role.
    - `GET`, `HEAD`, and `OPTIONS` requests are allowed for all users.
    - `DELETE` requests are only allowed for superusers.
    - All other methods require the user to be a staff member.

    Methods:
        has_permission(request, view) -> bool: Determines if the request should be permitted based on the method and user role.
    """

    def has_permission(self, request, view):
        """
       Checks whether the user has permission to perform the requested action.

       This method checks the request method and the user's role to determine if the action is allowed.

       Args:
           request (Request): The request object containing details of the request.
           view (APIView): The view that is handling the request.

       Returns:
           bool: True if the request is allowed, False otherwise.
       """
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        elif request.method == "DELETE":
            return request.user.is_superuser
        return request.user.is_staff
