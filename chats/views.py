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
    query = req.GET.get('query') if req.GET.get('query') != None else ''
    contacts = CustomUser.objects.filter(
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(role__name__icontains=query)
    ).exclude(id=req.user.id)

    other_user = CustomUser.objects.get(id=pk)

    context = {
        'chat_page': 'active',
        'contacts': contacts,
        'other_user': other_user,

    }

    return render(req, 'chats/chat_page.html', context)
