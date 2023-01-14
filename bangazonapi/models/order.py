from django.db import models
from .store import Store
from .user import User
from .payment_method import PaymentMethod

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_on = models.DateField(auto_now_add=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
