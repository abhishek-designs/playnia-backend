from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer
from .models import User 

# Create your views here.
@api_view(['POST'])
def sign_up_user(request):
    """
        View to register a user
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Get the user auth token
        auth_token = Token.objects.get(user=user)
        # Remove the password as well for security purpose
        user_res = serializer.data
        user_res.pop('password')
        user_res['auth-token'] = auth_token.key
        return Response(user_res, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sign_in_user(request):
    """
        View to login a user
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # User is valid get the token
        user = serializer.validated_data
        auth_token = Token.objects.get(user=user)
        return Response({'msg': 'Sign in successful', 'auth_token': auth_token.key}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_user_profile(request):
    """
        View to fetch registered user's data through auth token
    """
    # Serialize the user instance
    serializer = UserSerializer(request.user, many=False)
    user_res = serializer.data
    user_res.pop('password')
    return Response(user_res, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_user(request, pk):
    """
        View to fetch user with user id
    """
    # Serialize the user instance
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        user_res = serializer.data
        user_res.pop('password')
        return Response(user_res, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'msg': f'User with user id: {pk} not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
        View to fetch registered user's data through auth token
    """
    # Updating the user profile
    serializer = UserSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User updated!!'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

