from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from base.models import Notification
from django.contrib.contenttypes.models import ContentType
from .models import *
from django.db.models import Q
from django.db.models import Max


@login_required(login_url='login')
def chats(req):
    context = {
        'chats_page': 'active',
        'title': 'Chats',
    }
    return render(req, 'chats/index.html', context)


@login_required(login_url='login')
def threads(req):
    user = req.user

    # Get distinct thread IDs
    threads = ChatThread.objects.filter(
        Q(initiator=user) | Q(responder=user)
    ).annotate(latest_message=Max('chatmessage__timestamp')).order_by('-latest_message').distinct()

    context = {
        'threads': threads,
    }
    return render(req, 'chats/partials/threads.html', context)


@login_required(login_url='login')
def thread(req, pk):
    curr_user = req.user
    other_user = get_object_or_404(CustomUser, id=pk)

    # Attempt to retrieve the thread
    curr_thread = ChatThread.objects.filter(
        Q(initiator=curr_user, responder=other_user) |
        Q(initiator=other_user, responder=curr_user)
    ).first()


    # If the thread doesn't exist, create a new one
    if curr_thread is None:
        curr_thread = ChatThread.objects.create(
            initiator=curr_user, responder=other_user)

    related_threads = ChatThread.objects.filter(
        Q(initiator=curr_user) |
        Q(responder=curr_user)
    ).exclude(id =curr_thread.id)

    messages = ChatMessage.objects.filter(
        thread=curr_thread).order_by('timestamp')

    received_msgs = messages.filter(sender=other_user)

    for obj in related_threads:
        obj.is_active = False
        obj.save()

    for obj in received_msgs:
        obj.is_read = True
        obj.save()

        # Mark associated notifications as read
        associated_notifications = Notification.objects.filter(
            content_type=ContentType.objects.get_for_model(ChatMessage), object_id=obj.id)
        associated_notifications.update(is_read=True)

    context = {
        'chats_page': 'active',
        'curr_thread': curr_thread,
        'other_user': other_user,
        'messages': messages,
    }

    return render(req, 'chats/thread.html', context)


@login_required(login_url='login')
def contacts(req):
    user = req.user
    contacts = CustomUser.objects.all().exclude(id=user.id)
    context = {'contacts': contacts}
    return render(req, 'chats/partials/contacts.html', context)


@login_required(login_url='login')
def groups(req):
    user = req.user
    groups = CustomUser.objects.all().exclude(id=user.id)
    context = {'groups': groups}
    return render(req, 'chats/partials/groups.html', context)


@login_required(login_url='login')
def mark_messages_and_notifications_as_read(req):
    user = req.user
    ChatMessage.objects.filter(receiver=req.user,
                               is_read=False).update(is_read=True)
    # Update unread notifications
    Notification.objects.filter(
        user=req.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})
