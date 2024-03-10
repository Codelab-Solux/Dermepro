import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from django.template.loader import get_template
from . models import *

class NotificationConsumer(AsyncWebsocketConsumer):
    # connects to the websocket consumer
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        self.room_name = f'user_{self.user.id}_notifications'
        # self.room_name = f'user_notifications'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        print(f'Channel name : {self.channel_name}')
        print(f'Room name : {self.room_name}')
        await self.accept()


    # disconnects from the websocket consumer
    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )
    
    async def new_visitor(self, event):
        # print(f"Novelle visite : de {event['text']}")
        # await self.send(text_data=event['text'])
        html = get_template('base/partials/notifications.html').render(
            context = {
                'guest':event['text']
            }
        )
        await self.send(text_data=html)
    
    async def new_appointment(self, event):
        # print(f"Novelle visite : de {event['text']}")
        # await self.send(text_data=event['text'])
        html = get_template('base/partials/notifications.html').render(
            context = {
                'guest':event['text']
            }
        )
        await self.send(text_data=html)
