import re
from django.db import models
from django.core.exceptions import ValidationError
from .user import User

def validate_card_number(value):
    """Validate credit card number"""
    if not re.match(r'^[0-9]{16}$', value):
        raise ValidationError('Invalid credit card number format. Use 16 digits')

def validate_expiration_date(value):
    """Validates the expiration date format
"""
    if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{4}$', value):
        raise ValidationError('Invalid expiration date format. Use MM/YYYY')

class PaymentMethod(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16, validators=[validate_card_number])
    expiration_date = models.CharField(max_length=7, validators=[validate_expiration_date])
