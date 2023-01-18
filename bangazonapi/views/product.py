from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import Product, Store, Category

class ProductSerializer(serializers.ModelSerializer):
  """JSON serializer for products """
  store = serializers.SerializerMethodField()
  product_type = serializers.SerializerMethodField()
  price = serializers.SerializerMethodField()
  class Meta:
    model = Product
    fields = ('id', 'title', 'description', 'price', 'inventory', 'image', 'store', 'product_type')
  
  def get_store(self, obj):
    return obj.store.name
  
  def get_product_type(self, obj):
    return obj.product_type.label
  
  def get_price(self, obj):
    # format the obj.price value as a string with 2 decimal places, and a "$" sign in front of it.
    return f"${obj.price:.2f}".format(obj.price)
  
class ProductSerializerLimited(ProductSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price')


    
class ProductView(ViewSet):
  def list(self, request):
    """List products"""
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    """GET single product"""
    try:
      product = Product.objects.get(pk=pk)
      serializer = ProductSerializer(product)
      return Response(serializer.data)
    except Product.DoesNotExist:
      return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
  def update(self, request, pk):
    """Update a product"""
    product = Product.objects.get(pk=pk)
    product.title = request.data["title"]
    product.description = request.data["description"]
    product.price = request.data["price"]
    product.product_type = Category.objects.get(pk=request.data["product_type"])
    product.inventory = request.data["inventory"]
    product.image = request.data["image"]
    
    product.save()
    
    return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
  
  def create(self, request):
    """Creat a new product for the users store"""
    try:
      product = Product.objects.create(
        title = request.data["title"],
        description = request.data["description"],
        store = Store.objects.get(pk=request.data["store"]),
        price = request.data["price"],
        product_type = Category.objects.get(pk=request.data["product_type"]),
        inventory = request.data["inventory"],
        image = request.data["image"]
      )
      serializer = ProductSerializer(product)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
      return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
  def destroy(self, request, pk):
    """Delete a product"""
    product = Product.objects.get(pk=pk)
    product.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    
