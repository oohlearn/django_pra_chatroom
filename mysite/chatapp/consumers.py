from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
import re
from .models import ChatMessage, Room
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #async def connect(self):：定義connect方法，這是當WebSocket連接建立時自動調用的異步方法。

        self.room_name = self.scope['url_route']['kwargs']['room_name']
# 從scope中獲取room_name，scope是一個字典，包含了當前連接的所有信息。在這裡，room_name是從URL路由中提取的參數。  

        # 將當前的WebSocket連接添加到一個名為self.
        self.room_group_name = 'chat_%s' % re.sub(r'[^a-zA-Z0-9\-.]', '', self.room_name)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["roomName"]
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room
            })
        await self.save_message(username, message, room)
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        await self.send(text_data=json.dumps({
           'message': message,
           'username': username,
           'room': room
        }))
        
    @sync_to_async
    def save_message(self, username, message, room):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        ChatMessage.objects.create(user=user, message=message, room=room)
