import logging
from datetime import datetime
from django.http import HttpResponse

logging.basicConfig(filename="app_logs.txt", level=logging.DEBUG)


class BadRequestMiddleware:
    """
    Middleware to log requests resulting in bad or server error responses (HTTP 400 or 500).
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or view function to call.
        """
        self.get_response = get_response

    def __call__(self, request) -> 'HttpResponse':
        """
        Process the request and log if a 400 or 500 status code is returned.

        Args:
            request: The incoming HTTP request.

        Returns:
            response: The HTTP response object after processing.
        """
        response = self.get_response(request)
        if response.status_code == 400 or response.status_code == 500:
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Request processed with code {response.status_code}")
        return response


class UnauthorizedRequestMiddleware:
    """
    Middleware to log unauthorized access attempts (when user is anonymous).
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or view function to call.
        """
        self.get_response = get_response

    def __call__(self, request) -> 'HttpResponse':
        """
        Process the request and log if the user is unauthorized (anonymous).

        Args:
            request: The incoming HTTP request.

        Returns:
            response: The HTTP response object after processing.
        """
        if request.user.is_anonymous:
            logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Unauthorized attempt to access protected resource.")
        response = self.get_response(request)
        return response
