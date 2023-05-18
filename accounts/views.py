from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import *
# Create your views here.


def signupView(req):
    if req.user.is_authenticated:
        return redirect('home')

    form = SignupForm()
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "Votre compte vien d'être créé.")
            return redirect('login')
    else:
        form = SignupForm()
    context = {
        "signup_page": "active",
        "title": 'signup',
        'form': form,
    }
    return render(req, 'accounts/signup.html', context)


def loginView(req):
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.info(req, 'Username or Password is incorrect!')
    context = {
        "login_page": "active",
        "title": 'login'}
    return render(req, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(req):
    logout(req)
    return redirect('login')


@login_required(login_url='login')
def users(req):
    # new_users = CustomUser.objects.all().order_by('date_joined')[:18]
    new_users = CustomUser.objects.all()[:18]
    users = CustomUser.objects.all()

    if req.user.role.sec_level >= 6:
        form = CreateUserForm()
        if req.method == 'POST':
            form = CreateUserForm(req.POST)
            if form.is_valid():
                form.save()
                messages.success(req, "Le nouveau compte vien d'être créé.")
                return redirect('users')
        else:
            form = CreateUserForm()
    else:
        form = None

    ordering = ['last_name']
    context = {
        "users_page": "active",
        'title': 'users',
        'new_users': new_users,
        'users': users,
        'form': form,
        'ordering': ordering,
    }
    return render(req, 'accounts/users.html', context)


@ login_required(login_url='login')
def user_profile(req, pk):
    user = req.user
    profile = CustomUser.objects.get(id=pk)

    if user == profile:
        form = EditUserForm(instance=profile)
        if req.method == 'POST':
            form = EditUserForm(req.POST, req.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('users')

    if user.role.sec_level >= 6:
        form = AdminEditUserForm(instance=profile)
        if req.method == 'POST':
            form = AdminEditUserForm(req.POST, req.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('users')
    else:
        form = None
    context = {
        "rdv_page": "active",
        'title': 'appointment_detail',
        'profile': profile,
        'form': form,
    }
    return render(req, 'accounts/profile.html', context)

# ajax views----------------------------------------------------------------------------------


class AjaxRolesView(ListView):
    model = Role
    template_name = 'ajax_params.html'
    context_object_name = 'user_roles'


class AjaxCreateRole(View):
    def get(self, req):
        _name = req.GET.get('name', None)
        _fr_name = req.GET.get('fr_name', None)
        _sec_level = req.GET.get('sec_level', None)

        obj = Role.objects.create(
            name=_name,
            fr_name=_fr_name,
            sec_level=_sec_level
        )

        user_role = {
            'id': obj.id,
            'name': obj.name,
            'fr_name': obj.fr_name,
            'sec_level': obj.sec_level,
        }

        data = {
            'user_role': user_role
        }

        return JsonResponse(data)


class AjaxUpdateRole(View):
    def get(self, req):
        _id = req.GET.get('id', None)
        _name = req.GET.get('name', None)
        _fr_name = req.GET.get('fr_name', None)
        _sec_level = req.GET.get('sec_level', None)

        obj = Role.objects.get(id=_id)
        obj.name = _name,
        obj.fr_name = _fr_name,
        obj.sec_level = _sec_level
        obj.save()

        user_role = {
            'id': obj.id,
            'name': obj.name,
            'fr_name': obj.fr_name,
            'sec_level': obj.sec_level,
        }

        data = {
            'user_role': user_role
        }

        return JsonResponse(data)


class AjaxDeleteRole(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Role.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
