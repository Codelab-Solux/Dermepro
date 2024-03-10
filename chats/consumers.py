import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from .models import *

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        curr_user_id = int(self.scope['user'].id)
        other_user_id = int(self.scope['url_route']['kwargs']['id', 0])
        self.room_name = f'{min(curr_user_id, other_user_id)}-{max(curr_user_id, other_user_id)}'
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message = data['message']
            receiver = data['receiver']
            sender = data['sender']
            await self.save_message(sender, receiver, message, self.room_group_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'receiver': receiver,
                    'sender': sender,
                }
            )
        except json.JSONDecodeError:
            pass  # Handle JSON decoding error gracefully

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'receiver': event['receiver'],
            'sender': event['sender'],
        }))

    @DatabaseSyncToAsync
    def save_message(self, sender, receiver, message, thread):
        chat_obj = ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            thread=thread,
        )
        other_user_id = int(self.scope['url_route']['kwargs']['id'])
        get_other_user = CustomUser.objects.get(id=other_user_id)
        if receiver == get_other_user.id:
            ChatNotification.objects.create(chat=chat_obj, user=get_other_user)
