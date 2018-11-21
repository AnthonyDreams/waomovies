from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from apps.notificaciones.consumers import EchoConsumer

application = ProtocolTypeRouter({
	"websocket": URLRouter([
		re_path("ws/", EchoConsumer),
		])
	})