from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from bangazonapi.models import PaymentMethod, User

class PaymentMethodSerializer(serializers.ModelSerializer):
  class Meta:
        model = PaymentMethod
        fields = ('id', 'customer', 'label', 'card_number', 'expiration_date')

class PaymentMethodView(ViewSet):
  def list(self, request):
    """Get all of a user's payment methods"""
    customer = request.query_params.get('customer', None)
    if customer is not None:
      payment_methods = PaymentMethod.objects.filter(customer=customer)
    else:
      return Response({'error': 'Invalid customer'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    """Get a single payment method"""
    try:
      payment_method = PaymentMethod.objects.get(pk=pk)
      serializer = PaymentMethodSerializer(payment_method)
      return Response(serializer.data)
    except PaymentMethod.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
  
  def update(self, request, pk):
    """Update a customer's payment method"""
    payment_method = PaymentMethod.objects.get(pk=pk)
    payment_method.label = request.data["label"]
    payment_method.card_number = request.data["card_number"]
    payment_method.expiration_date= request.data["expiration_date"]
    
    payment_method.save()
    return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
  
  def create(self, request):
    """Create a new payment method"""
    try:
      payment_method = PaymentMethod.objects.create(
        label=request.data["label"],
        customer= User.objects.get(pk=request.data["customer"]),
        card_number=request.data["card_number"],
        expiration_date=request.data["expiration_date"],
      )
      serializer = PaymentMethodSerializer(payment_method)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
      return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
  def destroy(self, request, pk):
    """Delete a payment method"""
    payment_method = PaymentMethod.objects.get(pk=pk)
    payment_method.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
