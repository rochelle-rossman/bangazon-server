from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import ProductOrder


class ProductOrderSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = ProductOrder
    fields = ('id', 'product', 'order', 'quantity')
    depth = 1

class ProductOrderView(ViewSet):
  def list(self, request):
    """GET all product orders"""
    product = request.query_params.get('product')
    order = request.query_params.get('order')
    customer = request.query_params.get('customer')
    product_orders = ProductOrder.objects.all()
    if product is not None:
      product_orders = product_orders.filter(product=product)
    if order is not None:
      product_orders = product_orders.filter(order=order)
    if customer is not None:
      product_orders = product_orders.filter(order__customer=customer)
    serializer = ProductOrderSerializer(product_orders, many=True)
    return Response(serializer.data)
