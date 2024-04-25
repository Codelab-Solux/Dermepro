from calendar import calendar
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from base.models import Company
from base.templatetags.base_tags import *
from .forms import *
from .models import CustomUser
from datetime import datetime
from base.views import get_date_from_day_number, get_day_number_from_date, get_month_from_week, paginate_objects


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
            messages.error(req, 'Email ou Mots de passe incorrect!!!')
    context = {
        "login_page": "active",
        "title": 'Login'}
    return render(req, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(req):
    profile = req.user.profile
    profile.is_online = False
    profile.save()
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
        'title': 'Users',
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
        messages.success(req, "Nouveau compte créé!")
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/basic_form.html', context={'form': form, 'form_title': 'Créer un Utilisateur'})


@login_required(login_url='login')
def edit_user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)

    if user != curr_obj and not user.is_superuser:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    form = EditUserForm(instance=curr_obj)
    if req.method == 'POST':
        form = EditUserForm(req.POST, instance=curr_obj)
        if form.is_valid():
            print(form)
            form.save()
        messages.success(req, 'Utilisateur modifié avec success!')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/basic_form.html', context={'form': form, 'form_title': 'Modifier un Utilisateur', 'curr_obj': curr_obj})


@login_required(login_url='login')
def edit_profile(req, pk):
    curr_obj = get_object_or_404(Profile, id=pk)

    form = EditProfileForm(instance=curr_obj)
    if req.method == 'POST':
        form = EditProfileForm(req.POST, instance=curr_obj)
        if form.is_valid():
            print('saved')
            form.save()
        messages.success(req, 'Profil modifiée avec success')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'accounts/forms/profile_form.html', context={'form': form, 'form_title': 'Modifier ce profil', 'curr_obj': curr_obj})


@login_required(login_url='login')
@require_http_methods(['DELETE'])# secures the delete route and makes it only accessible by the DELETE method
def delete_user(req, pk):
    curr_obj = get_object_or_404(CustomUser, id=pk)
    if req.user.role.sec_level < 6:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    messages.success(req, 'Utilisateur supprimé  avec success!')
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def users_status_quo(req):
    unavailable_users = Profile.objects.filter(status=3)
    busy_users = Profile.objects.filter(status=2)
    context = {
        "unavailable_users": unavailable_users,
        "busy_users": busy_users,
    }
    return render(req, 'accounts/partials/users_status_quo.html', context)


@login_required(login_url='login')
def change_user_status(req, pk):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    new_status = get_object_or_404(UserStatus, id=pk)

    curr_profile.status = new_status
    curr_profile.save()
    messages.success(req, 'User Status changed!')
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def users_list(req, pk):
    users = CustomUser.objects.all().order_by('last_name')
    context = {"users": users}
    if pk == 'users':
        return render(req, 'accounts/partials/users_list.html', context)
    else:
        return render(req, 'accounts/partials/users_list_alt.html', context)


@login_required(login_url='login')
def user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)
    visit_hours = get_total_visits_minutes(curr_obj)
    appt_hours = get_total_appointment_minutes(curr_obj)

    context = {
        "user_detail_page": "active",
        'title': 'User Details',
        'curr_obj': curr_obj,
        'visit_hours': visit_hours,
        'appt_hours': appt_hours,
    }
    return render(req, 'accounts/profile_alt.html', context)


@login_required(login_url='login')
def profile(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)
    curr_profile = get_object_or_404(Profile, user=curr_obj)
    if user == curr_obj:
        is_self = True
    else:
        is_self = False

    context = {
        "user_profile_page": "active",
        'title': 'User Profile',
        'is_self': is_self,
        'curr_obj': curr_obj,
        'curr_profile': curr_profile,
    }
    return render(req, 'accounts/profile.html', context)


def filter_users(req, pk):
    user_role = req.POST.get('user_role')
    user_phone = req.POST.get('user_phone')
    last_name = req.POST.get('last_name')
    first_name = req.POST.get('first_name')
    user_status = req.POST.get('user_status')
    user_sex = req.POST.get('user_sex')
    user_presence = req.POST.get('user_presence')

    # Construct the base query
    base_query = CustomUser.objects.all().order_by('-last_name')

    # Apply filters based on parameters
    if user_role:
        base_query = base_query.filter(role_id=user_role)
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
    if user_presence:
        base_query = base_query.filter(
            profile__is_onsite=user_presence.title())

    users = base_query
    context = {"users": users}
    if pk == 'users':
        return render(req, 'accounts/partials/users_list.html', context)
    else:
        return render(req, 'accounts/partials/users_list_alt.html', context)


@login_required(login_url='login')
def time_mgt(req):
    TimeManagements = TimeManagement.objects.all().order_by('-date', '-time')
    users = CustomUser.objects.all()
    user_roles = Role.objects.all()

    context = {
        "time_mgt_page": "active",
        'title': 'Time Management',
        'TimeManagements': TimeManagements,
        'users': users,
        'user_roles': user_roles,
    }
    return render(req, 'accounts/time_mgt.html', context)


def time_mgt_details(req, pk):
    curr_user = get_object_or_404(CustomUser, id=pk)
    curr_date = datetime.today()
    day = get_day_number_from_date(curr_date)

    context = {
        "time_mgt_details_page": "active",
        'title': 'User Times',
        'day': day,
        'curr_user': curr_user,
        'curr_date': curr_date,
    }
    return render(req, 'accounts/time_mgt_details.html', context)


@login_required(login_url='login')
def manage_time(req, pk):
    user = get_object_or_404(CustomUser, id=pk)
    curr_profile = get_object_or_404(Profile, user=user)
    if curr_profile.is_onsite:
        movement = 'exit'
    else:
        movement = 'entry'

    signature = req.FILES.get('image', None)

    if signature:
        TimeManagement.objects.create(
            user=user,
            date=datetime.today(),
            time=timezone.now(),
            movement=movement,
            signature=signature
        )
    else:
        TimeManagement.objects.create(
            user=user,
            date=datetime.today(),
            time=timezone.now(),
            movement=movement,
        )

    messages.success(req, 'User TimeManagement changed!')
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def new_time_record(req):
    if req.method == 'POST':
        user_id = req.POST.get('user_id', None)
        user_password = req.POST.get('user_password', None)
        user = get_object_or_404(CustomUser, id=user_id)
        curr_profile = get_object_or_404(Profile, user=user)

        if curr_profile.is_onsite:
            movement = 'exit'
        else:
            movement = 'entry'
        hashed_password = user.password
        password_is_valid = check_password(user_password, hashed_password)
        if password_is_valid:
            TimeManagement.objects.create(
                user=user,
                user_password=hashed_password,
                date=datetime.today(),
                time=timezone.now(),
                movement=movement,
            )
            messages.success(req, 'User TimeManagement changed!')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            messages.error(req, 'Mots de pass incorect!')
            return HttpResponse(status=305, headers={'HX-Trigger': 'db_changed'})
    else:
        users = CustomUser.objects.all()
        context = {'users': users}
        return render(req, 'accounts/forms/time_mgt_form.html', context)


@login_required(login_url='login')
def create_time_mgt(req):

    form = TimeManagementForm()
    if req.method == 'POST':
        form = TimeManagementForm(req.POST)
        user = form.instance.user
        profile = get_object_or_404(Profile, user=user)
        if profile.is_onsite:
            form.instance.movement = 'exit'
        else:
            form.instance.movement = 'entry'
        
        if form.user_password == user.password:
            if form.is_valid():
                form.save()
            messages.success = 'Nouveau movement enrégistré!'
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            return JsonResponse({'success': False, 'error': 'Mots de pass incorect'})
    else:
        return render(req, 'base/forms/basic_form.html', context={'form': form, 'form_title': 'Gestion de temps'})



@login_required(login_url='login')
def time_records(req, pk):
    user = get_object_or_404(CustomUser, id=pk)
    curr_date = datetime.today()
    day = get_day_number_from_date(curr_date)
    time_records = TimeManagement.objects.filter(
        user=user, date=curr_date).order_by('-date', '-time')
    objects = paginate_objects(req, time_records)
    context = {
        "objects": objects,
        "curr_user": user,
        "curr_date": curr_date.date,
        "day": day,
    }
    return render(req, 'accounts/partials/time_records.html', context)


@login_required(login_url='login')
def filter_time_records(req, pk):
    user = get_object_or_404(CustomUser, id=pk)

    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    movement = req.POST.get('movement')

    base_query = TimeManagement.objects.filter(user=user)
    if min_date_query:
        base_query = base_query.filter(date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(date__lte=max_date_query)
    if movement:
        base_query = base_query.filter(
            movement=movement.title())

    objects = paginate_objects(req, base_query.order_by('-time'))
    context = {
        "objects": objects,
    }
    return render(req, 'accounts/partials/time_records.html', context)


@login_required(login_url='login')
def daily_time_records(req, pk, day=None):
    curr_user = get_object_or_404(CustomUser, id=pk)

    if day:
        curr_date = get_date_from_day_number(datetime.today().year, day)
    else:
        curr_date = datetime.today()
        day = get_day_number_from_date(curr_date)

    time_records = TimeManagement.objects.filter(
        user=curr_user, date=curr_date).order_by('-time')
    objects = paginate_objects(req, time_records)
    context = {
        "objects": objects,
        "curr_user": curr_user,
        "curr_date": curr_date,
        "day": day,
    }
    return render(req, 'accounts/partials/time_records.html', context)


def calendar_times(req):
    curr_company = Company.objects.first()
    starts_at = curr_company.opening_time.hour
    ends_at = curr_company.closing_time.hour
    if not starts_at:
        starts_at = 8
    if not ends_at:
        ends_at = 18

    hours = list(range(starts_at, ends_at + 1))

    curr_date = datetime.today().date()

    time_records = TimeManagement.objects.filter(date=curr_date).order_by('-time')
    
    objects = paginate_objects(req, time_records)

    # print(time_records)
    context = {
        "objects": objects,
        "curr_date": curr_date,
        "objects": objects,
        "time_records": time_records,
        "hours": hours,
    }
    return render(req, 'accounts/partials/calendar_times.html', context)
    

def filter_calendar_times(req,  pk=None,  day=None):
    curr_company = Company.objects.first()
    starts_at = curr_company.opening_time.hour
    ends_at = curr_company.closing_time.hour
    if not starts_at:
        starts_at = 8
    if not ends_at:
        ends_at = 18

    hours = list(range(starts_at, ends_at + 1))
    
    if day:
        curr_date = get_date_from_day_number(datetime.today().year, day)
    else:
        curr_date = datetime.today()

    if pk:
        curr_user = get_object_or_404(CustomUser, id=pk)
        time_records = TimeManagement.objects.filter(
            user=curr_user, date=curr_date).order_by('-time')
    else:
        time_records = TimeManagement.objects.filter(date=curr_date).order_by('-time')
    
    objects = paginate_objects(req, time_records)
    context = {
        "objects": objects,
        "curr_user": curr_user,
        "curr_date": curr_date,
        "objects": objects,
        "time_records": time_records,
        "hours": hours,
    }
    return render(req, 'accounts/partials/calendar_times.html', context)
    
