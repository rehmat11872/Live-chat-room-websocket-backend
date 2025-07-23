"""
ASGI config for chatproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# chatproject/asgi.py
# chatproject/asgi.py
import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Import routing AFTER django.setup()
try:
    import room_chat.routing
    print("✅ Successfully imported room_chat.routing")
    print(f"📋 WebSocket patterns: {room_chat.routing.websocket_urlpatterns}")
except ImportError as e:
    print(f"❌ Failed to import room_chat.routing: {e}")

django_asgi_app = get_asgi_application()

# Test the URL pattern manually
import re
pattern = r'ws/chat/(?P<room_name>[\w-]+)/$'
test_path = 'ws/chat/python-room/'
match = re.match(pattern, test_path)
print(f"🧪 Pattern test: '{pattern}' matches '{test_path}': {bool(match)}")
if match:
    print(f"🎯 Extracted room_name: {match.group('room_name')}")

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                room_chat.routing.websocket_urlpatterns
            )
        )
    ),
})

print("✅ ASGI application configured")
