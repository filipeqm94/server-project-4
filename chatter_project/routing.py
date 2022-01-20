from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator
from chatter.consumers import ChatConsumer

application = ProtocolTypeRouter({
  'websocket': AllowedHostsOriginValidator(
    URLRouter(
      [
        url('', ChatConsumer)
      ]
    )
  )
})