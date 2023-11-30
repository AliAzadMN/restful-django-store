from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not (value.isdigit() and len(value) == 11 and value.startswith('09')):
        raise ValidationError("Invalid phone number. Please enter a vaild phone number!")
        