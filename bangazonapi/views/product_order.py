from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import ProductOrder, Product, Order, Store, PaymentMethod, User, Category

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ('id', 'label')

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'street_address', 'city', 'state', 'zipcode')
class StoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Store
    fields = ('id', 'name')

class PaymentMethodSerializer(serializers.ModelSerializer):
  class Meta:
    model = PaymentMethod
    fields = ('id', 'label')

class ProductSerializer(serializers.ModelSerializer):
  store = StoreSerializer()
  product_type = CategorySerializer()

  class Meta:
    model = Product
    fields = ('id', 'title', 'price', 'image', 'store', 'product_type')

class OrderSerializer(serializers.ModelSerializer):
  customer = serializers.StringRelatedField()
  payment_method = PaymentMethodSerializer()
  products = ProductSerializer(many=True)
  store = StoreSerializer()
  customer = UserSerializer()

  class Meta:
    model = Order
    fields = ('id', 'ordered_on', 'status', 'store', 'customer', 'payment_method', 'products')

class ProductOrderSerializer(serializers.ModelSerializer):
  product = ProductSerializer()
  order = OrderSerializer()

  class Meta:
    model = ProductOrder
    fields = ('id', 'product', 'order', 'quantity')

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
