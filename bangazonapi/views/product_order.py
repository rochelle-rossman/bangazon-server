from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import ProductOrder


class ProductOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductOrder
    fields = ('id', 'product', 'order', 'quantity')

class ProductOrderView(ViewSet):
  def list(self, request):
    """GET all product orders"""
    product_orders = ProductOrder.objects.all()
    serializer = ProductOrderSerializer(product_orders, many=True)
    return Response(serializer.data)
