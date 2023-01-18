from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
  card_number = serializers.SerializerMethodField()
  class Meta:
        model = PaymentMethod
        fields = ('id', 'customer', 'label', 'card_number', 'expiration_date')
        
  def get_card_number(self, obj):
    card_number = obj.card_number
    last_four_digits = obj.card_number[-4:]
    obscured_card_number = "**** **** **** " + last_four_digits
    return obscured_card_number

class PaymentMethodView(ViewSet):
  def list(self, request):
    """Get all of a user's payment methods"""
    payment_methods = PaymentMethod.objects.all()
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)
    
