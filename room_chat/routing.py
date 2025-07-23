# room_chat/routing.py
from django.urls import re_path
from . import consumers

print("🔗 Loading WebSocket routing...")

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]

# print(f"📋 Loaded {len(websocket_urlpatterns)} WebSocket URL patterns")
# for pattern in websocket_urlpatterns:
#     print(f"  - {pattern.pattern.pattern}")
