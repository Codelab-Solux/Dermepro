
import json
from channels.generic.websocket  import AsyncWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from . models import *


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = int(self.scope['user'].id)
        other_user_id = int(self.scope['url_route']['kwargs']['id'])
        if my_id > other_user_id:
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        receiver = data['receiver']
        sender  = data['sender'] 

        await self.save_message(sender, message, self.room_group_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'receiver':receiver,
                'sender ':sender,

            }
        )

    async def chat_message(self, event):
        message = event['message']
        receiver = event['receiver']
        # sender = event['sender']

        await self.send(text_data= json.dumps({
                'message':message,
                'receiver':receiver,
                # 'sender ':sender,

            }))
        
    @DatabaseSyncToAsync
    def save_message(self, sender, message, thread_name):
        ChatMessage.objects.create(
            sender=sender, 
            message=message,
            thread_name=thread_name, 
        )


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        self.room_group_name = f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
