import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from .models import *
from django.db.models import Q
from base.models import Notification
from accounts.models import CustomUser


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def fetch_thread(self):
        curr_user = await sync_to_async(CustomUser.objects.get)(id=int(self.scope['user'].id))
        other_user = await sync_to_async(CustomUser.objects.get)(
            id=int(self.scope['url_route']['kwargs']['id']))
        try:
            active_thread = await sync_to_async(ChatThread.objects.get)(
                Q(initiator=curr_user, responder=other_user) |
                Q(initiator=other_user, responder=curr_user)
            )
            return active_thread
        except ChatThread.DoesNotExist:
            return None
    
    async def connect(self):
        curr_user_id = int(self.scope['user'].id)
        other_user_id = int(self.scope['url_route']['kwargs']['id'])
        self.room_name = f'{min(curr_user_id, other_user_id)}-{max(curr_user_id, other_user_id)}'
        self.room_group_name = f'room_group_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        thread = await self.fetch_thread()
        if thread is not None:
            thread.is_active = True
            await sync_to_async(thread.save)()
            print(f'thread {thread.id} activated')
        print(f"Correspondent = {other_user_id}")
        print(f"Chatroom = {self.room_name}")
        print(f"Chatgroup = {self.room_group_name}")

    async def disconnect(self, close_code):
        thread = await self.fetch_thread()
        if thread is not None:
            thread.is_active = False
            await sync_to_async(thread.save)()
            print(f'thread {thread.id} deactivated')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            message = data['message']
            receiver = data['receiver']
            sender = data['sender']
            thread_id = data['thread_id'] 
            await self.save_message( sender, receiver, message, thread_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender,
                    'receiver': receiver,
                    'message': message,
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

    async def save_message(self, sender, receiver, message, thread_id):
        print(f'thread ID : {thread_id}')
        print(f'sender ID : {sender}')
        print(f'receiver ID : {receiver}')
        print(f'message : {message}')
        try:  
            # Fetch the sender and receiver from CustomUser model
            sender_instance = await sync_to_async(CustomUser.objects.get)(id=sender)
            receiver_instance = await sync_to_async(CustomUser.objects.get)(id=receiver)
            
            # Fetch the chat thread
            thread = await sync_to_async(ChatThread.objects.get)(id=thread_id)

            # Create the ChatMessage object
            chat_obj = await sync_to_async(ChatMessage.objects.create)(
                sender=sender_instance,  # Pass the sender instance
                receiver=receiver_instance,
                message=message,
                thread=thread,
            )

            # Create Notification if the receiver is the other user
            if receiver == receiver_instance.id:
                await sync_to_async(Notification.objects.create)(
                    content_object=chat_obj,
                    object_id=chat_obj.id,
                    user=receiver_instance
                )    
        except CustomUser.DoesNotExist:
            # Handle user not found gracefully
            error_message = "User not found."
            await self.send_error_message(error_message)
        except ChatThread.DoesNotExist:
            # Handle chat thread not found gracefully
            error_message = "Chat thread not found."
            await self.send_error_message(error_message)
        except ObjectDoesNotExist:
            # Handle other ObjectDoesNotExist exceptions
            error_message = "Object not found."
            await self.send_error_message(error_message)


    async def send_error_message(self, error_message):
        # Send the error message to the client
        await self.send(text_data=json.dumps({
            'error': error_message
        }))
    
    # async def notify_message(self, event):
    #     await self.send(text_data=json.dumps({
    #         'message': event['message'],
    #         'sender': event['sender'],
    #     }))