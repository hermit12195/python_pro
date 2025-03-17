from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Custom validator for phone numbers
    value: int
    """
    if len(value) != 12 and not isinstance(value, int):
        raise ValidationError("Enter a valid phone number (12 digits).")
