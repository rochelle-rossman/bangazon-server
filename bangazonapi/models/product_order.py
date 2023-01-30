from django.db import models
from .order import Order
from .product import Product

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.deduct_from_inventory(self.quantity)
        
    def delete(self, *args, **kwargs):
        self.update_inventory_on_delete(self)
        super().delete(*args, **kwargs)
        
    @staticmethod
    def update_inventory_on_delete(productOrder):
        product = productOrder.product
        product.inventory += productOrder.quantity
        product.save()

