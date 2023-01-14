from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=40)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    created_on = models.DateField()
