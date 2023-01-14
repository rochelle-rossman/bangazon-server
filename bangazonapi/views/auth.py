from rest_framework.decorators import api_view
from rest_framework.response import Response
from bangazonapi.models import User


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User exists

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    try:
        user = User.objects.get(uid=uid)

    # If authentication was successful, respond with their token
        data = {
            'id': user.id,
            'uid': user.uid,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_on': user.created_on,
            'street_address': user.street_address,
            'city': user.city,
            'state': user.state,
            'zipcode': user.zipcode,
        }
        return Response(data)
    except:
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    # Now save the user info in the rareapi_user table
    user = User.objects.create(
        uid=request.data['uid'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        created_on=request.data['created_on'],
        street_address=request.data['street_address'],
        city=request.data['city'],
        state=request.data['state'],
        zipcode=request.data['zipcode']
    )

    # Return the user info to the client
    data = {
            'id': user.id,
            'uid': user.uid,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_on': user.created_on,
            'street_address': user.street_address,
            'city': user.city,
            'state': user.state,
            'zipcode': user.zipcode,
        }
    return Response(data)
