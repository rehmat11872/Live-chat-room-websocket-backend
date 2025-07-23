# room_chat/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            
            print(f"🔌 New connection to room: {self.room_name}")
            
            # Create room if it doesn't exist
            await self.create_room()
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            print(f"✅ Connection accepted for room: {self.room_name}")
            
            # Send recent messages after a small delay to ensure connection is stable
            await asyncio.sleep(0.1)
            recent_messages = await self.get_recent_messages()
            await self.send(text_data=json.dumps({
                'type': 'recent_messages',
                'messages': recent_messages
            }))
            
        except Exception as e:
            print(f"❌ Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        print(f"🔌 Disconnecting from room: {self.room_name}, code: {close_code}")
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"❌ Error in disconnect: {e}")

    async def receive(self, text_data):
        print(f"📨 Received message: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                message = text_data_json.get('message', '').strip()
                username = text_data_json.get('username', 'Anonymous').strip()
                
                if not message or not username:
                    print("❌ Invalid message or username")
                    return
                
                print(f"💬 Chat message from {username}: {message}")
                
                # Save message to database
                saved_message = await self.save_message(username, message)
                
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': username,
                        'timestamp': saved_message.timestamp.isoformat()
                    }
                )
                print(f"📤 Message broadcast to group: {self.room_group_name}")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")

    async def chat_message(self, event):
        try:
            message = event['message']
            username = event['username']
            timestamp = event.get('timestamp', '')
            
            print(f"📡 Broadcasting to client: {username}: {message}")
            
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timestamp
            }))
        except Exception as e:
            print(f"❌ Error broadcasting message: {e}")

    @database_sync_to_async
    def create_room(self):
        try:
            room, created = ChatRoom.objects.get_or_create(name=self.room_name)
            print(f"🏠 Room {'created' if created else 'found'}: {room.name}")
            return room
        except Exception as e:
            print(f"❌ Error creating room: {e}")
            raise

    @database_sync_to_async
    def save_message(self, username, message):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            msg = Message.objects.create(
                room=room,
                user=username,
                content=message
            )
            print(f"💾 Message saved with ID: {msg.id}")
            return msg
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            raise

    @database_sync_to_async
    def get_recent_messages(self):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
            msg_list = [
                {
                    'username': msg.user,
                    'message': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in reversed(messages)
            ]
            print(f"📜 Retrieved {len(msg_list)} recent messages")
            return msg_list
        except ChatRoom.DoesNotExist:
            print("🏠 Room doesn't exist, returning empty messages")
            return []
        except Exception as e:
            print(f"❌ Error getting recent messages: {e}")
            return []
