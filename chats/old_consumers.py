from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
from accounts.models import CustomUser
from .models import Message, Thread
import json

# class ChatConsumer(WebsocketConsumer):
#     async def connect(self):
#         self.accept()

#         self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'you are now connected'
#         }))

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         print('Message:', message)

#         self.send(text_data=json.dumps({
#             'type': 'chat',
#             'message': message
#         }))


# group chat consumer
class EchoConsumer(SyncConsumer):
    async def websocket_connect(self, event):
        self.room_name = 'broadcast'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })
        print(f'[{self.channel_name}] - You are connected')

    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - You received a message - {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': event.get('text')
            }
        )

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - You sent a message - {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name)
        print(event)


# private chat consumer
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = await sync_to_async(CustomUser.objects.get(username=other_username))

        self.thread_obj = await sync_to_async(Thread.objects.get_or_create_personal_thread(
            me, other_user))

        self.room_name = f'personal_thread_{self.thread_obj.id}'

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

        print(f'[{self.channel_name}] - You are connected')

    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - You received a message - {event["text"]}')
        msg = json.dumps({
            'text': event.get('text'),
            'username': self.scope['user'.username]
        })
        self.store_message(event.get('text'))
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': msg
            }
        )

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - You sent a message - {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name)
        print(event)

    def store_message(self, text):
        Message.objects.create(
            thread=self.thread_obj,
            sender=self.scope['user'],
            text=text
        )
