from  django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .store import Store
from .category import Category

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)])
    product_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products', height_field=None,
                                   width_field=None, max_length=None, null=True, blank=True)
