from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserLobbySerializer
from accounts.serializers import UserSerializer
from .models import UserLobby

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_lobby(request):
    """
        View to create a lobby and join the first user who created it
    """
    # Passing user data as context who created the lobby
    serializer = UserLobbySerializer(data=request.data,context={
        'user': request.user
    })
    if serializer.is_valid():
        lobby = serializer.save()
        return Response({'msg': f'{str(lobby)} lobby created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_lobbies(request):
    """
        View to fetch all the lobbies with the users joined in it
    """
    lobbies = UserLobby.objects.all()
    serializer = UserLobbySerializer(lobbies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def fetch_lobby(request, pk):
    """
        View to fetch a single lobby
    """
    try:
        lobby = UserLobby.objects.get(id=pk)
        serializer = UserLobbySerializer(lobby, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserLobby.DoesNotExist:
        return Response({'msg': f'Lobby with id: {pk} does not exists'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_lobby(request, pk):
    """
        View to join/follow the lobby
    """
    try:
        lobby = UserLobby.objects.get(id=pk)
        user = request.user
        user_serializer = UserSerializer(user, many=False)
        user_id = user_serializer.data['id']
        # Check wether this already exist or not
        user_exists = bool(lobby.users.filter(id=user_id))
        if user_exists:
            # Check existance of user in lobby
            return Response({ 'msg': f'User {user_id} already exists in this lobby' }, status=status.HTTP_409_CONFLICT)
        elif user == lobby.created_by:
            # Check wether this user is owner or not
            return Response({ 'msg': 'You are already an owner of this lobby' }, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            # Join the user to lobby
            lobby.users.add(user)
            lobby.followers_count = lobby.users.count()
            lobby.save()
            return Response({ 'msg': f'User now joined in Lobby {pk}' }, status=status.HTTP_200_OK)
    except UserLobby.DoesNotExist:
        return Response({ 'msg': f'Lobby with id: {pk} does not exists' }, status=status.HTTP_404_NOT_FOUND) 

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def exit_lobby(request, pk):
    """
        View to left the lobby
    """
    try:
        lobby = UserLobby.objects.get(id=pk)
        user = request.user
        if user == lobby.created_by:
            # User is the owner of this lobby
            return Response({ 'msg': "You are already an owner of this lobby you can't left" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Remove the user from lobby
            lobby.users.remove(user)
            lobby.followers_count = lobby.users.count()
            lobby.save()
            return Response({ 'msg': "You have left the lobby successfuly" }, status=status.HTTP_200_OK)
    except UserLobby.DoesNotExist:
        return Response({ 'msg': f'Lobby with id: {pk} does not exists' }, status=status.HTTP_404_NOT_FOUND) 

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_lobby(request, pk):
    """
        View to delete a lobby, this can only be done by the owner of this lobby
    """
    try:
        lobby = UserLobby.objects.get(id=pk)
        user = request.user
        if not user == lobby.created_by:
            # This user is not the owner of this lobby
            return Response({ 'msg': "Sorry you can't delete because you are not the owner of this lobby" },status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Owner can delete this
            lobby.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except UserLobby.DoesNotExist:
         return Response({ 'msg': f'Lobby with id: {pk} does not exists' }, status=status.HTTP_404_NOT_FOUND) 
