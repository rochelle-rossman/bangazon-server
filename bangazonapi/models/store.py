from django.db import models
from .user import User

class Store(models.Model):
    """A user can only have one store"""
    seller = models.OneToOneField(User, to_field='uid', unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
