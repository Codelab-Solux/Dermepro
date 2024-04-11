import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from django.template.loader import get_template
from asgiref.sync import sync_to_async
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
        # Update user's online status
        user_profile = await sync_to_async(Profile.objects.get)(user=self.user)
        user_profile.is_online = True
        await sync_to_async(user_profile.save)()
        print(f'user is online: {user_profile.is_online}')
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
    
    async def notify_visit(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'sex': event['data']['sex'],
            'person': event['data']['person'],
            'schedule': event['data']['schedule'],
        }))

    async def notify_visit_status(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'sex': event['data']['sex'],
            'person': event['data']['person'],
            'schedule': event['data']['schedule'],
        }))
    
    async def notify_appointment(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'sex': event['data']['sex'],
            'person': event['data']['person'],
            'schedule': event['data']['schedule'],
        }))

    async def notify_appointment_status(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'sex': event['data']['sex'],
            'person': event['data']['person'],
            'schedule': event['data']['schedule'],
        }))
    
    async def notify_message(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'message': event['data']['message'],
            'sender': event['data']['sender'],
        }))

    async def notify_new_user(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'user': event['data']['user'],
        }))

    async def notify_user_status(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'user': event['data']['user'],
        }))

    async def notify_user_auth(self, event):
        await self.send(text_data=json.dumps({
            'id': event['data']['id'],
            'type': event['data']['type'],
            'user': event['data']['user'],
        }))

    async def ping_user(self, user_id):
        user = await sync_to_async(CustomUser.objects.get)(id=user_id)
        notification_message = f"You have been pinged by {self.scope['user'].username}"
        # Here you can send the notification to the user
        await self.send(text_data=json.dumps({
            'type': 'ping',
            'message': notification_message,
        }))
        print('pinged')
