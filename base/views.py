from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from accounts.forms import RoleForm
from accounts.models import *
from .models import *
from .forms import *
import csv
# Create your views here.


@login_required(login_url='login')
def home(req):
    user = req.user
    if user.role.sec_level >= 4:
        curr_visits = Visit.objects.filter(status=2)
        # pending_visits = Visit.objects.filter(status=1)
        curr_rdvs = Appointment.objects.filter(status=2)
        pending_rdvs = Appointment.objects.filter(
            is_vip=False, status=1)
        pending_vips = Appointment.objects.filter(
            is_vip=True, status=1)

    else:
        curr_visits = Visit.objects.filter(host=user, status=2)
        curr_rdvs = []
        pending_rdvs = []
        pending_vips = []

    ordering = ['date']
    context = {
        "home_page": "active",
        'title': 'Home',
        # 'pending_visits': pending_visits,
        'curr_visits': curr_visits,
        'pending_rdvs': pending_rdvs,
        'pending_vips': pending_vips,
        'curr_rdvs': curr_rdvs,
        'ordering': ordering,
    }
    return render(req, 'base/index.html', context)

@login_required(login_url='login')
def visits(req):
    user = req.user
    statuses = Status.objects.all()
    hosts = CustomUser.objects.all()
    if user.role.sec_level >= 4:
        visits = Visit.objects.all().order_by('-date','-arrived_at')
    else:
        visits = Visit.objects.filter(host=user).order_by('-date','-arrived_at')
    context = {
        "visits_page": "active",
        'title': 'Visits',
        'visits': visits,                           
        'statuses': statuses,
        "hosts" : hosts,
    }
    return render(req, 'base/visits.html', context)

@login_required(login_url='login')
def visit(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Visit, id=pk)

    context = {
        "visit_details_page": "active",
        'title': 'Visit Details',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/visit.html', context)

@login_required(login_url='login')
def create_visit(req):
    user = req.user

    if user.role.sec_level < 4:
        return redirect('visits')

    form = VisitForm()
    if req.method == 'POST':
        form = VisitForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouvelle visit ajoutée!'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Visite'})

@login_required(login_url='login')
def edit_visit(req, pk):
    user = req.user
    # if user.role.sec_level < 4:
    #     return redirect('visits')

    curr_obj = get_object_or_404(Visit, id=pk)

    form = VisitForm(instance=curr_obj)
    if req.method == 'POST':
        form = VisitForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Visite', 'curr_obj': curr_obj})



# @login_required(login_url='login')
# def add_visit(req):
#     user = req.user

#     form = VisitForm()
#     if req.method == 'POST':
#         form = VisitForm(req.POST)
#         if form.is_valid():
#             form.save()
#         messages.success = 'Nouvelle visite ajoutée'
#         visits = Visit.objects.all()
#         return render(req, 'base/partials/visit_list.html', context={'visits': visits})
#     else:
#         return render(req, 'base/components/basic_form_alt.html', context={'form': form, 'target':'visit_list'})


@login_required(login_url='login')
@require_http_methods(['DELETE']) #secures the delete route and makes it only accessible by the DELETE method
def delete_visit(req, pk):
    curr_obj = get_object_or_404(Visit, id=pk)
    if req.user.role.sec_level < 4:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    success = 'Deleted successfully'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def visit_csv(req):
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachement; filename=visites.csv'
    # create csv writer
    writer = csv.writer(res)
    # designate the model(s) of interest
    visits = Visit.objects.all()
    # add column headings
    writer.writerow(['Hôte', 'Visiteur', 'Téléphone',
                    'Nationalité', 'Date', 'Arrivée', 'Départ', 'Sexe', 'Document', 'N° Document', 'Status'])
    for v in visits:
        writer.writerow([v.host.username, v.guest, v.tel, v.nationality, v.date,
                        v.arrived_at, v.departed_at, v.gender, v.id_doc, v.doc_num, v.status])

    return res


@ login_required(login_url='login')
def appointments(req):
    user = req.user
    if user.role.sec_level >= 3:
        appointments = Appointment.objects.all()
        closed_appointments = Appointment.objects.filter(
            status=3).order_by('date')[:15]

    else:
        return redirect(req.META.get('HTTP_REFERER', '/'))

    query = req.GET.get('query') if req.GET.get('query') != None else ''
    appointments = Appointment.objects.filter(
        Q(guest__icontains=query)
        | Q(tel__icontains=query)
        | Q(host__first_name__icontains=query)
    ).order_by('-date','-arrived_at')

    ordering = ['date']
    context = {
        "rdvs_page": "active",
        'title': 'appointments',
        'appointments': appointments,
        'closed_appointments': closed_appointments,
        'ordering': ordering,
    }
    return render(req, 'base/appointments.html', context)


@ login_required(login_url='login')
def appointment(req, pk):
    user = req.user
    curr_obj = Appointment.objects.get(id=pk)

    context = {
        "rdv_page": "active",
        'title': 'Appointment Details',
        'curr_obj': curr_obj,

    }
    return render(req, 'base/appointment.html', context)


@login_required(login_url='login')
def create_appointment(req):
    user = req.user

    if user.role.sec_level < 4:
        return redirect('appointments')

    form = AppointmentForm()
    if req.method == 'POST':
        form = AppointmentForm(req.POST)
        form.instance.status = 1
        if form.is_valid():
            form.save()
            return redirect('appointments')

    context = {
        "create_visit_page": "active",
        'title': 'create_visit',
        'form': form,
    }
    return render(req, 'base/appointment.html', context)


@login_required(login_url='login')
def edit_appointment(req, pk):
    user = req.user
    # if user.role.sec_level < 4:
    #     return redirect('visits')

    curr_obj = get_object_or_404(Appointment, id=pk)

    form = AppointmentForm(instance=curr_obj)
    if req.method == 'POST':
        form = AppointmentForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Rendez-vous', 'curr_obj': curr_obj})

        
@login_required(login_url='login')
@require_http_methods(['DELETE']) #secures the delete route and makes it only accessible by the DELETE method
def delete_appointment(req, pk):
    curr_obj = get_object_or_404(Appointment, id=pk)
    if req.user.role.sec_level < 5:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    success = 'Deleted successfully'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def appointments_csv(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect(req.META.get('HTTP_REFERER', '/'))

    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachement; filename=rendez_vous.csv'
    # create csv writer
    writer = csv.writer(res)
    # designate the model(s) of interest
    visits = Visit.objects.all()
    # add column headings
    writer.writerow(['Hôte', 'Visiteur', 'Téléphone',
                    'Nationalité', 'Date', 'Arrivée', 'Départ', 'Sexe', 'Document', 'N° Document', 'Status'])
    for v in visits:
        writer.writerow([v.host.username, v.guest, v.tel, v.nationality, v.date,
                        v.arrived_at, v.departed_at, v.gender, v.id_doc, v.doc_num, v.status])

    return res


@ login_required(login_url='login')
def dashboard(req):
    user = req.user
    if user.role.sec_level < 3:
        visits = Visit.objects.filter(host=user)
        users = CustomUser.objects.all()
        appointments = []
    else:
        appointments = Appointment.objects.all()
        visits = Visit.objects.all()
        users = CustomUser.objects.all()

    f_visits = int(Visit.objects.filter(gender='female').count())
    m_visits = int(Visit.objects.filter(gender='male').count())
    f_rdvs = int(Visit.objects.filter(gender='female').count())
    m_rdvs = int(Visit.objects.filter(gender='male').count())
    # most_visited= Visit.objects.filter(host='male')
    gender_list = ['Masculin', 'Feminin']
    visit_figs = [f_visits, m_visits]
    rdvs_stats = [f_rdvs, m_rdvs]

    labels = []
    data = []

    context = {
        "dash_page": "active",
        'title': 'appointments',
        'appointments': appointments,
        'visits': visits,
        'users': users,
        'gender_list': gender_list,
        'visit_figs': visit_figs,
        'rdvs_stats': rdvs_stats,
    }
    return render(req, 'base/dashboard.html', context)


@ login_required(login_url='login')
def parameters(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect(req.META.get('HTTP_REFERER', '/'))
    else:
        appointments = Appointment.objects.all()
        visits = Visit.objects.all()
        users = CustomUser.objects.all()
        user_roles = Role.objects.all()

    form = RoleForm()
    if req.method == 'POST':
        form = RoleForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('parameters')

    context = {
        "params_page": "active",
        'title': 'parameters',
        # 'rdv_types': rdv_types,
        # 'visit_types': visit_types,
        'user_roles': user_roles,
        'form': form,
    }
    return render(req, 'base/parameters.html', context)


@ login_required(login_url='login')
def role(req, pk):
    user = req.user
    curr_role = Role.objects.get(id=pk)
    if user.role.sec_level < 4:
        return redirect(req.META.get('HTTP_REFERER', '/'))

    form = RoleForm(instance=curr_role)
    if req.method == 'POST':
        form = RoleForm(req.POST, instance=curr_role)
        if form.is_valid():
            form.save()
            return redirect('parameters')
    context = {
        "user_role_page": "active",
        'title': 'user_role',
        'user_role': curr_role,
        'form': form,
    }
    return render(req, 'base/role.html', context)


@login_required(login_url='login')
def delete_role(req, pk):
    user_role = Role.objects.get(id=pk)
    if req.user.role.sec_level < 4:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    user_role.delete()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@ login_required(login_url='login')
def about(req):
    context = {
        "about_page": "active",
    }
    return render(req, 'base/about.html', context)


# notifications------------------------------------------------------------------------------------------------------

@login_required(login_url='login')
def notifications(req):
    notifications = ChatNotification.objects.filter(
        user=req.user, is_seen=False)
    users = CustomUser.objects.all()

    context = {
        'notifications': 'active',
        'notifications': notifications,
        'users': users,
    }
    return render(req, 'base/notifications.html', context)


@login_required(login_url='login')
def read_notification(req, pk):
    user = req.user
    obj = ChatNotification.objects.get(id=pk)
    if user != obj.user:
        return redirect(req.META.get('HTTP_REFERER', '/'))

    if req.method == 'POST':
        if obj.is_seen == False:
            ChatNotification.objects.filter(id=pk).update(is_seen=True)
            return redirect('chat_page', obj.chat.sender)
        else:
            return redirect(req.META.get('HTTP_REFERER', '/'))


# htmx partials ---------------------------------------------------------------------
@login_required(login_url='login')
def appointment_list(req):
    user = req.user
    if user.role.sec_level >= 4:
        appointments = Appointment.objects.all().order_by('-date','-time')
    else:
        appointments = Appointment.objects.filter(host=user).order_by('-date','-time')
    context = {"appointments" : appointments}
    return render(req, 'base/partials/appointment_list.html', context)

@login_required(login_url='login')
def pending_vips(req):
    appointments = Appointment.objects.filter(is_vip=True, status=1)
    context = {"appointments" : appointments}
    return render(req, 'base/partials/pending_vips.html', context)

@login_required(login_url='login')
def pending_appointments(req):
    appointments = Appointment.objects.filter(status=1).exclude(is_vip=True)
    context = {"appointments" : appointments}
    return render(req, 'base/partials/pending_appointments.html', context)

@login_required(login_url='login')
def ongoing_appointments(req):
    appointments = Appointment.objects.filter(status=2)
    context = {"appointments" : appointments}
    return render(req, 'base/partials/ongoing_appointments.html', context)

def filter_appointments(req):
    user = req.user
    appointments = Appointment.objects.all().order_by('-date','-time')
    query = req.POST.get('query')
    if query != "":
        appointments = Appointment.objects.filter(guest__icontains=query).order_by('-date','-time')

    context = {"appointments" : appointments}
    print(query)
    return render(req, 'base/partials/appointment_list.html', context)

@login_required(login_url='login')
def create_appointment(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect('home')

    form = AppointmentForm()
    if req.method == 'POST':
        form = AppointmentForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau rendez-vous ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/components/basic_form.html', context={'form': form, 'form_title' : 'Rendez-vous'})


@login_required(login_url='login')
def edit_appointment_status(req, pk, kp):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    curr_obj = get_object_or_404(Appointment, id=pk)
    new_status = get_object_or_404(Status, id=kp)
    curr_obj.status = new_status
    curr_obj.save()
    
    if kp==2:
        new_user_status = get_object_or_404(UserStatus, id=kp)
        curr_profile.status = new_user_status
        curr_profile.save()
    
    else:
        new_user_status = get_object_or_404(UserStatus, id=1)
        curr_profile.status = new_user_status
        curr_profile.save()
        print(curr_profile.status)

    context={'obj':curr_obj}
    return render(req, 'base/components/status_badge.html', context)

# visit ---------------------------------------------------------------------

@login_required(login_url='login')
def visit_list(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.all().order_by('-date','-arrived_at')
    else:
        visits = Visit.objects.filter(host=user).order_by('-date','-arrived_at')
    context = {"visits" : visits}
    return render(req, 'base/partials/visit_list.html', context)


@login_required(login_url='login')
def ongoing_visits(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.filter(status=2).order_by('-date','-arrived_at')
    else:
        visits = Visit.objects.filter(status=2, host=user).order_by('-date','-arrived_at')
    context = {"visits" : visits}
    return render(req, 'base/partials/ongoing_visits.html', context)


@login_required(login_url='login')
def pending_visits(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.filter(status=1).order_by('-date','-arrived_at')
    else:
        visits = Visit.objects.filter(status=1, host=user).order_by('-date','-arrived_at')
    context = {"visits" : visits}
    return render(req, 'base/partials/pending_visits.html', context)


def filter_visits(req):
    user = req.user
    query = req.POST.get('query')
    if user.role.sec_level >= 4:
        if query != "":
            # if user.role.sec_level >= 4:
            #     visits = Visit.objects.filter(
            #         Q(host__username__icontains=query)
            #         |Q(guest__icontains=query)
            #         | Q(gender__icontains=query)
            #         # | Q(date__icontains=query)
            #         # | Q(arrived_at__icontains=query)
            #         # | Q(departed_at__icontains=query)
            #         # | Q(nationality__icontains=query)
            #         | Q(context__icontains=query)
            #         | Q(status__title__icontains=query)
            #     ).order_by('-date','-arrived_at')
            # else:
            #     visits = Visit.objects.filter(
            #         Q(guest__icontains=query)
            #         | Q(gender__icontains=query)
            #         | Q(context__icontains=query)
            #         | Q(status__title__icontains=query), 
            #         host=user,
            #     ).order_by('-date','-arrived_at')
            visits = Visit.objects.filter(guest__icontains=query).order_by('-date','-arrived_at')
        else:    
            visits = Visit.objects.all().order_by('-date','-arrived_at')
    else :
        if query != "":
            visits = Visit.objects.filter(guest__icontains=query, host=user).order_by('-date','-arrived_at')
        else:    
            visits = Visit.objects.filter(host=user).order_by('-date','-arrived_at')

    context = {"visits" : visits}
    print(query)
    return render(req, 'base/partials/visit_list.html', context)
    

@login_required(login_url='login')
def edit_visit_status(req, pk, kp):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    curr_obj = get_object_or_404(Visit, id=pk)
    new_status = get_object_or_404(Status, id=kp)
    if user != curr_obj.host:
        return redirect('visits')

    curr_obj.status = new_status
    curr_obj.save()
    
    if kp==2:
        curr_obj.accepted_at = timezone.now()
        curr_obj.save()
        new_user_status = get_object_or_404(UserStatus, id=kp)
        curr_profile.status = new_user_status
        curr_profile.save()

    else:
        new_user_status = get_object_or_404(UserStatus, id=1)
        curr_profile.status = new_user_status
        curr_profile.save()

    context={'obj':curr_obj}
    return render(req, 'base/components/status_badge.html', context)
