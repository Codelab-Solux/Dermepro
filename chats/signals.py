from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatNotification
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        nottification_objs = ChatNotification.objects.filter(is_seen = False, user = instance.user)
        nottification_count = ChatNotification.objects.filter(is_seen = False, user = instance.user).count()
        user_id = str(instance.user)
        data = {
            'notifications':nottification_objs,
            'nottification_count':nottification_count
        }

        async_to_sync(channel_layer.group_send)(
            user_id,{
                'type':'send_notification',
                'value': json.dumps(data)
            }
        )
