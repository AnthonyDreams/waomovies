from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from apps.notificaciones.consumers import TickTockConsumer
from apps.notificaciones import routing
application = ProtocolTypeRouter({

    'websocket': AuthMiddlewareStack( 
    	URLRouter(
        routing.websocket_urlpatterns
    )
    	),

    })