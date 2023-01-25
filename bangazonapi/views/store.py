from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers, status
from bangazonapi.models import Store, User

class StoreSerializer(serializers.ModelSerializer):
  """JSON serializer for stores"""
  class Meta:
    model = Store
    fields = '__all__'
    depth = 1
    
class StoreView(ViewSet):
  def list(self, request):
    """List all stores"""
    seller = request.query_params.get('seller', None)
    if seller is not None:
        stores = Store.objects.filter(seller=seller)
    else:
        stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    """Retieve single store """
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StoreSerializer(store)
    return Response(serializer.data)

    
  def update(self, request, pk):
    """Update a single store"""
    store = Store.objects.get(pk=pk)
    store.name = request.data["name"]
    
    store.save()
    
    return Response(None, status=status.HTTP_202_ACCEPTED)
  
  def create(self, request):
    """Create a store for the authenticated user"""
    try:
      store = Store.objects.create(
        seller = User.objects.get(id=request.data["seller"]),
        name = request.data["name"]
      )
      serializer = StoreSerializer(store)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
      return Response({'message': e.args[0]},status=status.HTTP_400_BAD_REQUEST)
