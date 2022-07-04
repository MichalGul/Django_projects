from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
"""
ProtocolTypeRouter class provided by Channels as the main entry point of your routing system. 
ProtocolTypeRouter takes a dictionary that maps communication types like http or websocket to ASGI applications. 
"""

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
