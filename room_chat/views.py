from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatRoomDetailView(generics.RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    lookup_field = 'name'

class RoomMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        room_name = self.kwargs['room_name']
        try:
            room = ChatRoom.objects.get(name=room_name)
            return Message.objects.filter(room=room).order_by('timestamp')
        except ChatRoom.DoesNotExist:
            return Message.objects.none()

@api_view(['POST'])
def create_room(request):
    room_name = request.data.get('name')
    if not room_name:
        return Response({'error': 'Room name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    serializer = ChatRoomSerializer(room)
    
    if created:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_200_OK)