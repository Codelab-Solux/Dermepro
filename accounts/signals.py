
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=TimeManagement)
def change_user_presence(sender, instance, created, **kwargs):
    if created:
        curr_profile = instance.user.profile
        if curr_profile.is_onsite == True:
            curr_profile.is_onsite = False
            curr_profile.is_online = False
        else:
            curr_profile.is_onsite = True
            
        curr_profile.save()
