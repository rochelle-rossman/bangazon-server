"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users"""
    class Meta:
        model = User
        fields = '__all__'

class UserViewSet(ViewSet):
    def list(self, request):
        """List users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET single user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as exception:
            return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Update a user"""
        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.street_address = request.data["street_address"]
        user.city = request.data["city"]
        user.state = request.data["state"]
        user.zipcode = request.data["zipcode"]
        
        user.save()
        
        return Response(None, status=status.HTTP_202_ACCEPTED)
        
    def destroy(self, request, pk):
        """Delete a user"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
