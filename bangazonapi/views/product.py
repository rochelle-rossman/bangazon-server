from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import Product, Store, Category

class ProductSerializer(serializers.ModelSerializer):
  """JSON serializer for products """
  store = serializers.SerializerMethodField()
  product_type = serializers.SerializerMethodField()
  quantity = serializers.IntegerField(write_only=True)

  class Meta:
    model = Product
    fields = ('id', 'title', 'description', 'price', 'inventory', 'image', 'store', 'product_type', 'quantity')
  
  def get_store(self, obj):
    return {"name":obj.store.name, "id":obj.store.id}
  
  def get_product_type(self, obj):
    return obj.product_type.label
  
class ProductSerializerLimited(ProductSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price')


    
class ProductView(ViewSet):
  def list(self, request):
      """List products"""
      category = request.query_params.get('category')
      store = request.query_params.get('store')
      if category:
          products = Product.objects.filter(product_type__id=category)
      if store:
        products = Product.objects.filter(store=store)
      else:
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
    
    
    
