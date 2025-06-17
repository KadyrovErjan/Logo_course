from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_name>/',ChatConsumer.as_asgi()),
]
