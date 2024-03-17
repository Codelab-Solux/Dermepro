from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from accounts.models import CustomUser
from base.models import Notification
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
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
    new_users = CustomUser.objects.all()[:18]
    users = CustomUser.objects.all()
    user_roles = Role.objects.all()
    user_statuses = UserStatus.objects.all()

    ordering = ['last_name']
    context = {
        "users_page": "active",
        'title': 'users',
        'new_users': new_users,
        'users': users,
        'user_roles': user_roles,
        'user_statuses': user_statuses,
        'ordering': ordering,
    }
    return render(req, 'accounts/users.html', context)


@login_required(login_url='login')
def create_user(req):
    user = req.user

    if user.role.sec_level < 4:
        return redirect('visits')


    form = CreateUserForm()
    if req.method == 'POST':
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = "Nouveau compte créé!"
        return redirect('users')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Utilisateur'})



@login_required(login_url='login')
def edit_user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)

    if user != curr_obj and user.role.sec_level < 6:
        return redirect('visits')

    form = EditUserForm(instance=curr_obj)
    if req.method == 'POST':
        form = EditUserForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Rendez-vous', 'curr_obj': curr_obj})


@ login_required(login_url='login')
@require_http_methods(['DELETE']) #secures the delete route and makes it only accessible by the DELETE method
def delete_user(req, pk):
    curr_obj = get_object_or_404(CustomUser, id=pk)
    if req.user.role.sec_level < 6:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    success = 'Deleted successfully'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def unavailable_users(req):
    user_profiles = Profile.objects.filter(status=3)
    context = {"user_profiles" : user_profiles}
    return render(req, 'accounts/partials/unavailable_users.html', context)


@login_required(login_url='login')
def occupied_users(req):
    user_profiles = Profile.objects.filter(status=2)
    context = {"user_profiles" : user_profiles}
    return render(req, 'accounts/partials/occupied_users.html', context)


@login_required(login_url='login')
def change_user_status(req, pk):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    new_status = get_object_or_404(UserStatus, id=pk)

    curr_profile.status = new_status
    curr_profile.save()
    messages.success = 'User Status changed'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

def fetch_user_status(req):
    user = req.user
    status = user.profile.status.name  # Assuming 'name' is the attribute containing the status name
    return JsonResponse({'status': status})


@login_required(login_url='login')
def user_list(req):
    user = req.user
    users = CustomUser.objects.all().order_by('last_name')
    context = {"users" : users}
    return render(req, 'accounts/partials/user_list.html', context)


@ login_required(login_url='login')
def user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)

    context = {
        "user_detail_page": "active",
        'title': 'User Details',
        'curr_obj': curr_obj,
    }
    return render(req, 'accounts/user.html', context)
    

def filter_users(req):
    user = req.user
    user_type = req.POST.get('user_type')
    user_phone = req.POST.get('user_phone')
    last_name = req.POST.get('last_name')
    first_name = req.POST.get('first_name')
    user_status = req.POST.get('user_status')
    user_sex = req.POST.get('user_sex')
    
    # Construct the base query
    base_query = CustomUser.objects.all().order_by('-last_name')

    # Apply filters based on parameters
    if user_type:
        base_query = base_query.filter(role_id=user_type)
    if user_phone:
        base_query = base_query.filter(phone=user_phone)
    if last_name:
        base_query = base_query.filter(last_name__icontains=last_name)
    if first_name:
        base_query = base_query.filter(first_name__icontains=first_name)
    if user_status:
        base_query = base_query.filter(profile__status__id=user_status)
    if user_sex:
        base_query = base_query.filter(profile__sex=user_sex)

    users = base_query
    context = {"users" : users}
    print(users)
    return render(req, 'accounts/partials/user_list.html', context)
