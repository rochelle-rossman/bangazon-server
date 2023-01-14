from django.db import models
from .user import User

class Store(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
          
    def __str__(self):
        return self.name
