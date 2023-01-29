from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import ProductOrder, Product, Order


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
    order_status = request.query_params.get('status')
    product_orders = ProductOrder.objects.all()
    if order_status is not None:
      product_orders = product_orders.filter(order__status=order_status)
    if product is not None:
      product_orders = product_orders.filter(product=product)
    if order is not None:
      product_orders = product_orders.filter(order=order)
    if customer is not None:
      product_orders = product_orders.filter(order__customer=customer)
    serializer = ProductOrderSerializer(product_orders, many=True)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Update a productOrder"""
    product_order = ProductOrder.objects.get(pk=pk)
    product_order.product = Product.objects.get(pk=request.data["product"])
    product_order.order = Order.objects.get(pk=request.data['order'])
    product_order.quantity = request.data["quantity"]
    product_order.save()
    return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
  
  def destroy(self, request, pk):
    """Delete a productOrder"""
    product_order = ProductOrder.objects.get(pk=pk)
    product_order.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
