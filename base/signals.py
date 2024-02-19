import json
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         nottification_objs = ChatNotification.objects.filter(is_seen = False, user = instance.id)
#         nottification_count = ChatNotification.objects.filter(is_seen = False, user = instance.id).count()
#         user_id = str(instance.id)
#         data = {
#             'notifications':nottification_objs,
#             'nottification_count':nottification_count
#         }

#         async_to_sync(channel_layer.group_send)(
#             user_id,{
#                 'type':'send_notification',
#                 'value': json.dumps(data)
#             }
#         )

@receiver(post_save, sender= Visit)
def send_visit_notification(sender, instance, created, **kwargs):
    if created:
        # trigger notification to all consumers in the 'user_{user_id}_notifications' group
        user_id = str(instance.host.id)
        channel_layer = get_channel_layer()
        room_name = f'user_{user_id}_notifications'
        print(f'Signal sent to : {room_name}')
        # room_name = f'user_notifications'
        event = {
            'type':'new_visitor',
            'text': instance.guest
        }
        # async_to_sync(channel_layer.group_send)(room_name, event)
        async_to_sync(channel_layer.group_send)(room_name, event)

@receiver(post_save, sender= Appointment)
def send_appointment_notification(sender, instance, created, **kwargs):
    if created:
        # trigger notification to all consumers in the 'user_{user_id}_notifications' group
        user_id = str(instance.host.id)
        channel_layer = get_channel_layer()
        room_name = f'user_{user_id}_notifications'
        print(f'Signal sent to : {room_name}')
        # room_name = f'user_notifications'
        event = {
            'type':'new_appointment',
            'text': instance.guest
        }
        async_to_sync(channel_layer.group_send)(room_name, event)