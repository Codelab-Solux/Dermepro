import json
from base.models import *
from chats.models import *
from accounts.models import *
from django.db.models.signals import pre_save, post_save
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


@receiver(post_save, sender=Visit)
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
                'type':'visit',
                'sex': instance.sex ,
                'person': f'{instance.last_name} {instance.first_name}',
                'schedule': f'{instance.date} à {instance.arrived_at}',
            }
        }
        async_to_sync(channel_layer.group_send)(room_name, event)

    # if not created:
    #     # Check if the user's status has changed
    #     if instance.status_changed:
    #         # Get the security group
    #         security_group = Group.objects.get(name="Securité")
    #         authorized_users = security_group.user_set.all()
    #         for user in authorized_users:
    #             # Create a notification for each user
    #             notification = Notification.objects.create(
    #                 user=user,
    #                 content_object=instance,
    #                 # message=f"{instance.last_name} {instance.first_name}'s status has changed."
    #             )
    #             # Send the notification data to the WebSocket consumer
    #             channel_layer = get_channel_layer()
    #             room_name = f'user_{user.id}_notifications'
    #             event = {
    #             'type':'notify_visit_status',
    #             'data':{
    #                     'id':instance.id,
    #                     'type':'visit_status',
    #                     'sex': instance.sex ,
    #                     'person': f'{instance.last_name} {instance.first_name}',
    #                     'schedule': f'{instance.date} à {instance.arrived_at}',
    #                 }
    #             }
    #             async_to_sync(channel_layer.group_send)(room_name, event)


@receiver(post_save, sender=Appointment)
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
                'type':'appointment',
                'sex': instance.sex ,
                'person': f'{instance.last_name} {instance.first_name}',
                'schedule': f'{instance.date} à {instance.time}',
            }
        }
        async_to_sync(channel_layer.group_send)(room_name, event)


    # if not created:
    #     # Check if the user's status has changed
    #     if instance.status_changed:
    #         # Get the security group
    #         security_group = Group.objects.get(name="Securité")
    #         authorized_users = security_group.user_set.all()
    #         for user in authorized_users:
    #             # Create a notification for each user
    #             notification = Notification.objects.create(
    #                 user=user,
    #                 content_object=instance,
    #                 # message=f"{instance.last_name} {instance.first_name}'s status has changed."
    #             )
    #             # Send the notification data to the WebSocket consumer
    #             channel_layer = get_channel_layer()
    #             room_name = f'user_{user.id}_notifications'
    #             event = {
    #                 'type': 'notify_appointment_status',
    #                 'data': {
    #                     'id':instance.id,
    #                     'type':'appointment_status',
    #                     'sex': instance.sex ,
    #                     'person': f'{instance.last_name} {instance.first_name}',
    #                     'schedule': f'{instance.date} à {instance.time}',
    #                 },
    #             }
    #             async_to_sync(channel_layer.group_send)(room_name, event)


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


@receiver(post_save, sender=Profile)
def send_new_user_notification(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.all()
        for user in users:
            # Create a notification for each user
            notification = Notification.objects.create(
                user=user,
                content_object=instance,
                # message=f"{instance.last_name} {instance.first_name}'s status has changed."
            )
            # Send the notification data to the WebSocket consumer
            channel_layer = get_channel_layer()
            room_name = f'user_{user.id}_notifications'
            event = {
                'type': 'notify_new_user',
                'data': {
                    'id': instance.id,
                    'type': 'user',
                    'user': f'{instance.user.last_name} {instance.user.first_name}',
                },
            }
            async_to_sync(channel_layer.group_send)(room_name, event)


@receiver(pre_save, sender=Profile)
def send_user_status_notification(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Profile.objects.get(pk=instance.pk)
        print(f'old status {old_instance.status}')
        print(f'new status {instance.status}')
        if old_instance.status != instance.status:
            authorized_users = CustomUser.objects.filter(role__sec_level__gte=4)
            for user in authorized_users:
                # Create a notification for each user
                # notification = Notification.objects.create(
                #     user=user,
                #     content_object=instance,
                #     # message=f"{instance.last_name} {instance.first_name}'s status has changed."
                # )
                # Send the notification data to the WebSocket consumer
                channel_layer = get_channel_layer()
                room_name = f'user_{user.id}_notifications'
                event = {
                    'type': 'notify_user_status',
                    'data': {
                        'id': instance.id,
                        'type': 'status_quo',
                        'user': f'{instance.user.last_name} {instance.user.first_name}',
                        # 'status': instance.status
                    },
                }
                async_to_sync(channel_layer.group_send)(room_name, event)
