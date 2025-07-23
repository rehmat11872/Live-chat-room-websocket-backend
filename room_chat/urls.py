from django.urls import path
from . import views

urlpatterns = [
    path('api/rooms/', views.ChatRoomListCreateView.as_view(), name='room-list'),
    path('api/rooms/<str:name>/', views.ChatRoomDetailView.as_view(), name='room-detail'),
    path('api/rooms/<str:room_name>/messages/', views.RoomMessagesView.as_view(), name='room-messages'),
    path('api/create-room/', views.create_room, name='create-room'),
]