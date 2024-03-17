import json
from .models import *
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# @receiver(post_save, sender=ChatMessage)
# def send_chat_notification(sender, instance, created, **kwargs):
#     if created:
#         # Create a notification for the chat message
#         notification = Notification.objects.create(
#             user=instance.receiver,
#             content_object=instance,
#         )
#         # Send the notification data to the WebSocket consumer
#         channel_layer = get_channel_layer()
#         room_name = f'user_{instance.receiver.id}_notifications'
#         print(f'Chat notification sent to : {room_name}')
#         event = {
#             'type': 'notify_message',
#             'data': {
#                 'message': instance.message
#                 'sender': instance.sender
#             },
#         }
#         async_to_sync(channel_layer.group_send)(room_name, event)
