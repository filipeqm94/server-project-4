from typing import Protocol
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chatter.routing

application = ProtocolTypeRouter({
  'websocket': AuthMiddlewareStack(
    URLRouter(
      chatter.routing.websocket_urlpatterns
    )
  )
})