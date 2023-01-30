from  django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .store import Store
from .category import Category

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)])
    product_type = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    inventory = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)

    def deduct_from_inventory(self, quantity):
        if self.inventory >= quantity:
            self.inventory -= quantity
            self.save()
        else:
            raise ValueError("Not enough inventory to complete the order.")
