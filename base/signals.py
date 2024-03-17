import json
from base.models import *
from chats.models import *
from accounts.models import *
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Visit)
def set_missed_visit(sender, instance, created, **kwargs):
    if created:
        if instance.host.profile.status.id > 1:
            new_status = get_object_or_404(Status, id=4)
            instance.status = new_status
            instance.is_missed = True
            instance.save()
            print(instance.status)




@receiver(post_save, sender= Visit)
def send_visit_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the visit
        notification = Notification.objects.create(
            user=instance.host,
            content_object=instance,
        )
        # Send the notification data to the WebSocket consumer
        channel_layer = get_channel_layer()
        room_name = f'user_{instance.host.id}_notifications'
        print(f'Visit notification sent to : {room_name}')
        event = {
            'type':'notify_visit',
            'data':{
                'id':instance.id,
                'type':'appointment',
                'sex': instance.sex ,
                'person': f'{instance.last_name} {instance.first_name}',
                'schedule': f'{instance.date} à {instance.arrived_at}',
            }
        }
        async_to_sync(channel_layer.group_send)(room_name, event)




@receiver(post_save, sender= Appointment)
def send_appointment_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the appointment
        notification = Notification.objects.create(
            user=instance.host,
            content_object=instance,
        )
        # Send the notification data to the WebSocket consumer
        channel_layer = get_channel_layer()
        room_name = f'user_{instance.host.id}_notifications'
        print(f'Appointment notification sent to : {room_name}')
        event = {
            'type':'notify_appointment',
            'data':{
                'id':instance.id,
                'type':'visit',
                'sex': instance.sex ,
                'person': f'{instance.last_name} {instance.first_name}',
                'schedule': f'{instance.date} à {instance.time}',
            }
        }
        async_to_sync(channel_layer.group_send)(room_name, event)




@receiver(post_save, sender=ChatMessage)
def send_chat_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the chat message
        notification = Notification.objects.create(
            user=instance.receiver,
            content_object=instance,
        )
        # Send the notification data to the WebSocket consumer
        channel_layer = get_channel_layer()
        room_name = f'user_{instance.receiver.id}_notifications'
        print(f'Chat notification sent to : {room_name}')
        event = {
            'type': 'notify_message',
            'data': {
                'id':instance.id,
                'type':'chat',
                'thread_id': instance.thread.id,
                'message': instance.message,
                'sender': f'{instance.sender.last_name} {instance.sender.first_name}',
            },
        }
        async_to_sync(channel_layer.group_send)(room_name, event)