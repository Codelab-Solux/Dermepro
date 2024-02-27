from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404 ,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import *
from django.db.models import Q


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
    threads = ChatMessage.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    context = {'threads': threads}
    return render(req, 'chats/partials/threads.html', context)


@login_required(login_url='login')
def contacts(req):
    user = req.user
    contacts = CustomUser.objects.all().exclude(id=user.id)
    context = {'contacts':contacts}
    return render(req, 'chats/partials/contacts.html', context)


@login_required(login_url='login')
def groups(req):
    user = req.user
    groups = CustomUser.objects.all().exclude(id=user.id)
    context = {'groups':groups}
    return render(req, 'chats/partials/groups.html', context)


def thread(req, pk):
    curr_user = req.user
    other_user = get_object_or_404(CustomUser, id=pk)

    # Attempt to retrieve the thread
    thread = ChatThread.objects.filter(
        Q(initiator=curr_user, responder=other_user) |
        Q(initiator=other_user, responder=curr_user)
    ).first()

    # If the thread doesn't exist, create a new one
    if thread is None:
        thread = ChatThread.objects.create(initiator=curr_user, responder=other_user)

    messages = ChatMessage.objects.filter(thread=thread).order_by('-timestamp')

    context = {
        'chats_page': 'active',
        'other_user': other_user,
        'messages': messages,
        'thread': thread,
    }

    return render(req, 'chats/thread.html', context)

# @login_required(login_url='login')
# def thread(req, pk):

#     # threads = ChatMessage.objects.raw(f'''

#     #     SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id} ORDER BY timestamp DESC
#     # ''')
#     # SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id} AND ( SELECT DISTINCT (chats_chatmessage.thread_name) FROM chats_chatmessage) ORDER BY chatmessage.timestamp DESC;
#     # SELECT * FROM chats_chatmessage WHERE sender={user.id} OR receiver={user.id}
#     #           ORDER BY timestamp DESC;

#     threads = ChatMessage.objects.filter(
#         Q(sender=user) | Q(receiver=user)
#     ).order_by('thread_name', '-timestamp')

#     other_user = CustomUser.objects.get(id=pk)

#     if user.id > other_user.id:
#         thread_name = f'chat_{user.id}-{other_user.id}'
#     else:
#         thread_name = f'chat_{other_user.id}-{user.id}'

#     messages = ChatMessage.objects.filter(thread_name=thread_name)

#     # thread_other_user = CustomUser.objects.get()

#     context = {
#         'chat_page': 'active',
#         'contacts': contacts,
#         'other_user': other_user,
#         'messages': messages,
#         'threads': threads,
#         'users': users,

#     }

#     return render(req, 'chats/thread.html', context)
