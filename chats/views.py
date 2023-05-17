from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import *


@login_required(login_url='login')
def chats(req):
    contacts = CustomUser.objects.all()
    threads = Thread.objects.by_user(
        user=req.user).prefetch_related('chat_thread').order_by('updated_at')

    context = {
        'chats_page': 'active',
        'contacts': contacts,
        'threads': threads,
    }
    return render(req, 'chats/index.html', context)


@login_required(login_url='login')
def chat_box(req, pk):
    contacts = CustomUser.objects.all()
    threads = Thread.objects.by_user(
        user=req.user).prefetch_related('chat_thread').order_by('created_at')
    active_thread = Thread.objects.get(id=pk)

    context = {
        'chats_page': 'active',
        'contacts': contacts,
        'threads': threads,
        'active_thread': active_thread,


    }
    return render(req, 'chats/chat_box.html', context)


@login_required(login_url='login')
def create_thread(req, pk):
    user1 = req.user
    user2 = CustomUser.objects.get(id=pk)
    contacts = CustomUser.objects.all()
    threads = Thread.objects.by_user(
        user=req.user).prefetch_related('chat_thread').order_by('created_at')
    thread = Thread.objects.filter(first_person=user1, second_person=user2) | Thread.objects.filter(
        first_person=user2, second_person=user1)

    if not thread:
        thread = Thread.objects.create(first_person=user1, second_person=user2)

    context = {
        'active_thread': thread,
        'contacts': contacts,
        'threads': threads,
    }
    return render(req, 'chats/index.html', context)


@login_required(login_url='login')
def delete_text(req, pk):
    message = Message.objects.filter(id=pk, sender=req.user)
    if not message:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    message.delete()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


# ------------------------------ AJAX -----------------------------------------
@login_required(login_url='login')
def get_msgs(req, pk):
    active_thread = Thread.objects.get(id=pk)
    messages = Message.objects.filter(thread=active_thread)
    return JsonResponse({'text_msgs': list(messages.values())})
