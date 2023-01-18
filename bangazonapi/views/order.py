from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import Order, PaymentMethod, Product, Store, User, ProductOrder
from .product import ProductSerializerLimited
from .product_order import ProductOrderSerializer

class OrderSerializer(serializers.ModelSerializer):
  """JSON Serializer for Orders"""
  store = serializers.SerializerMethodField()
  payment_method = serializers.SerializerMethodField()
  customer = serializers.SerializerMethodField()
  products = ProductSerializerLimited(many=True)
  total = serializers.SerializerMethodField()

  class Meta:
    model = Order
    fields = ('id', 'store', 'customer', 'ordered_on', 'payment_method', 'products', 'status', 'total')
    
  def get_store(self, obj):
    return obj.store.name
  
  def get_customer(self, obj):
    return obj.customer.first_name, obj.customer.last_name, obj.customer.email
  
  def get_payment_method(self, obj):
    label = obj.payment_method.label
    last_four_digits = obj.payment_method.card_number[-4:]
    obscured_card_number = "**** **** **** " + last_four_digits
    return {"label": label, "card_number": obscured_card_number}
  
  def get_products(self, obj):
          products = obj.products.all()
          serializer = ProductSerializerLimited(products, many=True)
          return serializer.data
        
  def get_total(self, obj):
    total = 0
    for product in obj.products.all():
      try:
        product_order = ProductOrder.objects.get(order = obj, product = product)
        total += product_order.quantity * product.price
      except ProductOrder.DoesNotExist:
        pass
    return total
    
class OrderView(ViewSet):
  def list(self, request):
    """GET all orders"""
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    """Get a single order"""
    try:
      order = Order.objects.get(pk=pk)
      serialzer = OrderSerializer(order)
      return Response(serialzer.data)
    except Order.DoesNotExist:
      return Response({'message': 'No such order'}, status=status.HTTP_404_NOT_FOUND)
    

  def update(self, request, pk):
      order = Order.objects.get(pk=pk)
      old_status = order.status
      order.status = request.data["status"]
      order.payment_method = PaymentMethod.objects.get(id=request.data["payment_method"])
      product_ids = request.data["products"]
      if not isinstance(product_ids, list):
          raise ValidationError({"message": "products field must be a list"})

      for product in product_ids:
          if 'id' not in product or 'quantity' not in product:
              raise ValidationError({"message": "products field must contain id and quantity"})
          try:
              product_obj = Product.objects.get(id=product["id"])
          except Product.DoesNotExist:
              return Response({'message': f"Product {product['id']} does not exist"})
      products = Product.objects.filter(id__in=[product['id'] for product in product_ids])
      order.products.set(products)
      if order.status == "canceled" and old_status != "canceled":
          order.return_products()
      order.save()
      return Response(None, status=status.HTTP_202_ACCEPTED)

    
  def create(self, request):
      """Create a new Order"""
      products = request.data.get("products")

      try:
          store = Store.objects.get(pk=request.data["store"])
          customer = User.objects.get(uid=request.data["customer"])
          payment_method = PaymentMethod.objects.get(pk=request.data["payment_method"])
      except (Store.DoesNotExist, User.DoesNotExist, PaymentMethod.DoesNotExist):
          return Response({"message": "Invalid store, customer or payment_method id"},
                          status=status.HTTP_400_BAD_REQUEST)

      order = Order.objects.create(store=store, customer=customer, payment_method=payment_method)
      total = 0
      product_list = []
      for product in products:
          try:
              product_obj = Product.objects.get(id=product['id'])
          except Product.DoesNotExist:
              return Response({"message": f"Product {product['id']} does not exist"})
          product_obj.deduct_from_inventory(product['quantity'])
          ProductOrder.objects.create(product=product_obj, order=order, quantity=product['quantity'])
          product_list.append(product_obj)
          total += product_obj.price * product['quantity']
      order.products.add(*product_list)
      order.total = total
      order.save()
      serializer = OrderSerializer(order)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
