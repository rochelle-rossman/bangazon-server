from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .store import Store
from .user import User
from .payment_method import PaymentMethod
from django.apps import apps

class Order(models.Model):
    STATUS_CHOICES = (
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_on = models.DateField(auto_now_add=True, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField("Product", through="ProductOrder", related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-progress')

    def total(self):
        total = 0
        for product in self.products.all():
            total += product.price
        return total
    
    def return_products(self):
        if self.status == 'canceled':
            ProductOrder = apps.get_model('bangazonapi', 'ProductOrder')
            product_orders = ProductOrder.objects.filter(order=self)
            for product_order in product_orders:
                product = product_order.product
                product.deduct_from_inventory(-product_order.quantity)

            
@receiver(pre_save, sender=Order)
def set_ordered_on_to_null(sender, instance, **kwargs):
        if instance.status == 'in-progress':
            instance.ordered_on = None
pre_save.connect(set_ordered_on_to_null, sender=Order)
