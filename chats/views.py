from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import *
from django.db.models import Q


@login_required(login_url='login')
def chats(req):
    query = req.GET.get('query') if req.GET.get('query') != None else ''
    contacts = CustomUser.objects.filter(
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(role__name__icontains=query)
    ).exclude(id=req.user.id)

    context = {
        'chat': 'active',
        'contacts': contacts,
    }
    return render(req, 'chats/index.html', context)


@login_required(login_url='login')
def chat_page(req, pk):
    user = req.user
    users =CustomUser.objects.all()
    query = req.GET.get('query') if req.GET.get('query') != None else ''
    contacts = CustomUser.objects.filter(
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(role__name__icontains=query)
    ).exclude(id=req.user.id)

    # threads = ChatMessage.objects.raw(f'''

    #     SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id} ORDER BY timestamp DESC
    # ''')
        # SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id} AND ( SELECT DISTINCT (chats_chatmessage.thread_name) FROM chats_chatmessage) ORDER BY chatmessage.timestamp DESC;
        # SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id}  
        #           ORDER BY timestamp DESC;
        
    threads = ChatMessage.objects.filter(
        Q(sender = user.id) | Q(receiver = user.id)
    ).values().distinct('thread_name').order_by('thread_name','-timestamp')

    other_user = CustomUser.objects.get(id=pk)

    if user.id > other_user.id:
        thread_name = f'chat_{user.id}-{other_user.id}'
    else:
        thread_name = f'chat_{other_user.id}-{user.id}'

    messages = ChatMessage.objects.filter(thread_name=thread_name)


    # thread_other_user = CustomUser.objects.get()

    context = {
        'chat_page': 'active',
        'contacts': contacts,
        'other_user': other_user,
        'messages': messages,
        'threads': threads,
        'users': users,

    }

    return render(req, 'chats/chat_page.html', context)
