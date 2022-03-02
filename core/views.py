from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserLobbySerializer
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_lobbies(request):
    """
        View to fetch all the lobbies with the users joined in it
    """
    lobbies = UserLobby.objects.all()
    serializer = UserLobbySerializer(lobbies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

