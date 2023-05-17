from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, View

from accounts.forms import UserRoleForm
from accounts.models import UserRole
from .models import *
from .forms import *
import csv
# Create your views here.


@login_required(login_url='login')
def home(req):
    user = req.user
    if user.role == 'admin':
        visits = Visit.objects.filter(status='pending')
        curr_visits = Visit.objects.filter(status='open')
        curr_rdvs = Appointment.objects.filter(status='open')
        pending_rdvs = Appointment.objects.filter(
            is_vip=False, status='pending')
        pending_vips = Appointment.objects.filter(
            is_vip=True, status='pending')

    else:
        visits = Visit.objects.filter(host=user, status='pending')
        curr_visits = Visit.objects.filter(host=user, status='open')
        curr_rdvs = []
        pending_rdvs = []
        pending_vips = []

    ordering = ['date']
    context = {
        "home_page": "active",
        'title': 'home',
        'visits': visits,
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
    if user.role == 'admin':
        visits = Visit.objects.all()
        closed_visits = Visit.objects.filter(
            status='closed').order_by('date')[:18]
    else:
        visits = Visit.objects.filter(host=user)
        closed_visits = Visit.objects.filter(
            host=user, status='closed').order_by('date')[:18]

    # query = req.GET.get('query') if req.GET.get('query') != None else ''
    # visits = Visit.objects.filter(
    #     Q(guest__icontains=query)
    #     | Q(tel__icontains=query)
    #     | Q(host__first_name__icontains=query)
    # ).distinct()

    form = VisitForm()
    if req.method == 'POST':
        form = VisitForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('visits')

    ordering = ['date']
    context = {
        "visits_page": "active",
        'title': 'visits',
        'visits': visits,
        'closed_visits': closed_visits,
        'form': form,
        'ordering': ordering,
    }
    return render(req, 'base/visits.html', context)


@login_required(login_url='login')
def visit_detail(req, pk):
    user = req.user
    visit = Visit.objects.get(id=pk)
    if visit == None:
        return redirect('visits')

    if user.role != 'admin' and user != visit.host:
        return redirect('visits')

    form = EditVisitForm(instance=visit)
    if req.method == 'POST':
        form = EditVisitForm(req.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('visits')
    context = {
        "visit_page": "active",
        'title': 'visit_detail',
        'visit': visit,
        'form': form,
    }
    return render(req, 'base/visit_detail.html', context)


@login_required(login_url='login')
def delete_visit(req, pk):
    visit = Visit.objects.get(id=pk)
    if req.user.role != 'admin':
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    visit.delete()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


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
    if user.role == 'admin':
        appointments = Appointment.objects.all()
        pending_vips = Appointment.objects.filter(
            is_vip=True, status='pending').order_by('date')[:15]

    else:
        return redirect('home')

    query = req.GET.get('query') if req.GET.get('query') != None else ''
    appointments = Appointment.objects.filter(
        Q(guest__icontains=query)
        | Q(tel__icontains=query)
        | Q(host__first_name__icontains=query)
    ).distinct()

    form = AppointmentForm()
    if req.method == 'POST':
        form = AppointmentForm(req.POST)
        form.instance.host = user
        if form.is_valid():
            form.save()
            return redirect('appointments')

    ordering = ['date']
    context = {
        "rdvs_page": "active",
        'title': 'appointments',
        'appointments': appointments,
        'pending_vips': pending_vips,
        'form': form,
        'ordering': ordering,
    }
    return render(req, 'base/appointments.html', context)


@ login_required(login_url='login')
def appointment_detail(req, pk):
    user = req.user
    appointment = Appointment.objects.get(id=pk)
    if user != appointment.host:
        return redirect('home')

    form = EditAppointmentForm(instance=appointment)
    if req.method == 'POST':
        form = EditAppointmentForm(req.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments')
    context = {
        "rdv_page": "active",
        'title': 'appointment_detail',
        'appointment': appointment,
        'form': form,
    }
    return render(req, 'base/appointment_detail.html', context)


@login_required(login_url='login')
def delete_rdv(req, pk):
    appointment = Appointment.objects.get(id=pk)
    if req.user.role != 'admin':
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    appointment.delete()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def rdv_csv(req):
    user = req.user
    if user.role != 'admin':
        return redirect('home')

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
    if user.role == 'admin':
        appointments = Appointment.objects.all()
        visits = Visit.objects.all()
        users = CustomUser.objects.all()
    else:
        visits = Visit.objects.filter(host=user)
        users = CustomUser.objects.all()
        appointments = []

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
    if user.role == 'admin':
        appointments = Appointment.objects.all()
        visits = Visit.objects.all()
        users = CustomUser.objects.all()
        user_roles = UserRole.objects.all()
    else:
        return redirect('home')

    form = UserRoleForm()
    if req.method == 'POST':
        form = UserRoleForm(req.POST)
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
def role_detail(req, pk):
    user = req.user
    curr_role = UserRole.objects.get(id=pk)
    if user.role != 'admin':
        return redirect('home')

    form = UserRoleForm(instance=curr_role)
    if req.method == 'POST':
        form = UserRoleForm(req.POST, instance=curr_role)
        if form.is_valid():
            form.save()
            return redirect('parameters')
    context = {
        "user_role_page": "active",
        'title': 'user_role_detail',
        'user_role': curr_role,
        'form': form,
    }
    return render(req, 'base/role_detail.html', context)


@login_required(login_url='login')
def delete_role(req, pk):
    user_role = UserRole.objects.get(id=pk)
    if req.user.role != 'admin':
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    user_role.delete()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


@ login_required(login_url='login')
def about(req):
    context = {
        "about_page": "active",
    }
    return render(req, 'base/about.html', context)

# ajax views------------------------------------------------------------------------------------------------------
