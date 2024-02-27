from django.core.paginator import Paginator
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
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import csv, qrcode, base64
from datetime import datetime

# Create your views here.
def paginate_objects(req, obj_list, obj_count=10):
    paginator = Paginator(obj_list, obj_count)
    page_number = req.GET.get('page',1)
    objects = paginator.get_page(page_number)
    return objects

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

# visits --------------------------------------------------------------------------
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
                        v.arrived_at, v.departed_at, v.sex, v.id_doc, v.doc_num, v.status])

    return res

# appointments ---------------------------------------------------------------------
@ login_required(login_url='login')
def appointments(req):
    user = req.user
    hosts = CustomUser.objects.all()
    statuses = Status.objects.all()
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
        'statuses': statuses,
        'hosts': hosts,
        'ordering': ordering,
    }
    return render(req, 'base/appointments.html', context)

@ login_required(login_url='login')
def appointment(req, pk):
    user = req.user
    curr_obj = Appointment.objects.get(id=pk)

    context = {
        "appointment_details_page": "active",
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
                        v.arrived_at, v.departed_at, v.sex, v.id_doc, v.doc_num, v.status])

    return res

# dashboard ------------------------------------------------------------------------
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

    f_visits = int(Visit.objects.filter(sex='female').count())
    m_visits = int(Visit.objects.filter(sex='male').count())
    f_rdvs = int(Visit.objects.filter(sex='female').count())
    m_rdvs = int(Visit.objects.filter(sex='male').count())
    # most_visited= Visit.objects.filter(host='male')
    sex_list = ['Masculin', 'Feminin']
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
        'sex_list': sex_list,
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

# notifications----------------------------------------------------------------------
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
    host_query = req.POST.get('host')
    name_query = req.POST.get('name')
    status_query = req.POST.get('status')
    sex_query = req.POST.get('sex')
    
    # Construct the base query
    base_query = Appointment.objects.all().order_by('-date', '-time')

    # Apply filters based on parameters
    if user.role.sec_level >= 4:
        if host_query:
            base_query = base_query.filter(host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    if name_query:
        base_query = base_query.filter(guest__icontains=name_query)
    if status_query:
        base_query = base_query.filter(status__id=status_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)

    appointments = base_query
    context = {"appointments" : appointments}
    print(appointments)
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
    host_query = req.POST.get('host')
    name_query = req.POST.get('name')
    status_query = req.POST.get('status')
    type_query = req.POST.get('type')
    sex_query = req.POST.get('sex')
    
    # Construct the base query
    base_query = Visit.objects.all().order_by('-date', '-arrived_at')

    # Apply filters based on parameters
    if user.role.sec_level >= 4:
        if host_query:
            base_query = base_query.filter(host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    if name_query:
        base_query = base_query.filter(guest__icontains=name_query)
    if status_query:
        base_query = base_query.filter(status__id=status_query)
    if type_query:
        base_query = base_query.filter(context=type_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)

    visits = base_query

    context = {"visits": visits}
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

# reports ---------------------------------------------------------------------
@login_required(login_url='login')
def reports(req):
    user = req.user
    roles = Role.objects.all()
    hosts = CustomUser.objects.all()
    user_statuses = UserStatus.objects.all()
    statuses = Status.objects.all()

    context = {
        "report_page": "active",
        'title': 'Reports',
        'roles': roles,
        'hosts': hosts,
        'user_statuses': user_statuses,
        'statuses': statuses,
    }
    return render(req, 'base/reports.html', context)

def users_table(req):
    user = req.user
    users = CustomUser.objects.all()
    objects = paginate_objects(req, users)
    context = {'objects': objects}
    return render(req, 'base/partials/users_table.html', context)
    # return render(req, 'base/reports.html', context)

def filter_users_table(req):
    user = req.user
    role_query = req.POST.get('role')
    status_query = req.POST.get('status')
    last_name_query = req.POST.get('last_name')
    first_name_query = req.POST.get('first_name')
    sex_query = req.POST.get('sex')
    last_login_query = req.POST.get('last_login')
    
    # Construct the base query
    base_query = CustomUser.objects.all().order_by('-last_name', '-first_name')

    # Apply filters based on parameters
    if user.role.sec_level >= 4:
        if role_query:
            base_query = base_query.filter(role__id=role_query)

    if status_query:
        base_query = base_query.filter(profile__status__id=status_query)
    if last_name_query:
        base_query = base_query.filter(last_name__icontains=last_name_query)
    if first_name_query:
        base_query = base_query.filter(first_name__icontains=first_name_query)
    if sex_query:
        base_query = base_query.filter(profile__sex=sex_query)
    if last_login_query:
        base_query = base_query.filter(last_login__lte=last_login_query)

    users = base_query
    objects = paginate_objects(req, users)
    context = {'objects': objects}
    return render(req, 'base/partials/users_table.html', context)

def visits_table(req):
    user = req.user
    visits = Visit.objects.all().order_by('-date', '-arrived_at')
    objects = paginate_objects(req, visits)
    context = {'objects': objects}
    return render(req, 'base/partials/visits_table.html', context)
    # return render(req, 'base/reports.html', context)

def filter_visits_table(req):
    user = req.user
    # Get filter parameters from request
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    host_query = req.POST.get('host')
    type_query = req.POST.get('type')
    sex_query = req.POST.get('sex')
    status_query = req.POST.get('status')
    
    # Construct the base query
    base_query = Visit.objects.all().order_by('-date', '-arrived_at')

    # Apply filters based on parameters
    if user.role.sec_level >= 4:
        if host_query:
            base_query = base_query.filter(host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    # Apply filters based on parameters
    if min_date_query:
        base_query = base_query.filter(date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(date__lte=max_date_query)
    if type_query:
        base_query = base_query.filter(context=type_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)
    if status_query:
        base_query = base_query.filter(status__id=status_query)

    visits = base_query

    # If the request is for CSV export, generate and return CSV response
    if req.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="visites.csv"'
        writer = csv.writer(response)
        
        # Write header row
        writer.writerow(['Date', 'Hôte', 'Visiteur','Telephone', 'Sexe', 'Cadre', "Heure d'arrivée","Heure de debut","Heure de départ", "Status"])
        
        # Write data rows
        for visit in visits:
            writer.writerow([visit.date, visit.host.username, visit.guest, visit.tel, visit.sex, visit.context, visit.arrived_at, visit.accepted_at, visit.departed_at, visit.status])
        
        return response

    # For regular view rendering, paginate and return context
    objects = paginate_objects(req, visits)
    context = {'objects': objects}
    return render(req, 'base/partials/visits_table.html', context)

def appointments_table(req):
    user = req.user
    appointments = Appointment.objects.all().order_by('-date', '-time')
    objects = paginate_objects(req, appointments)
    context = {'objects': objects}
    return render(req, 'base/partials/appointments_table.html', context)
    # return render(req, 'base/reports.html', context)

def filter_appointments_table(req):
    user = req.user
    host_query = req.POST.get('host')
    status_query = req.POST.get('status')
    sex_query = req.POST.get('sex')
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    
    # Construct the base query
    base_query = Appointment.objects.all().order_by('-date', '-time')

    # Apply filters based on parameters
    if user.role.sec_level >= 4:
        if host_query:
            base_query = base_query.filter(host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    if status_query:
        base_query = base_query.filter(status__id=status_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)
    if min_date_query:
        base_query = base_query.filter(date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(date__lte=max_date_query)

    appointments = base_query
    objects = paginate_objects(req, appointments)
    context = {'objects': objects}
    return render(req, 'base/partials/appointments_table.html', context)

def generate_visit_badge(req, pk):
    curr_obj = get_object_or_404(Visit, id=pk)
    # Create QR code as before
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{curr_obj.guest}#{curr_obj.host}@{datetime.now()}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to base64 encoding
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    context= {
        'qr_code_base64': qr_code_base64,
        'curr_obj':curr_obj
        }
    
    return render(req, 'base/partials/visit_badge.html',context)

def sign_visit(req, pk):
    if req.method == 'POST':
        print("Received POST request to sign_visit")
        print("Request FILES:", req.FILES)  # Print request.FILES to inspect its contents
        if 'image' in req.FILES:
            curr_obj = Visit.objects.get(id=pk)  # Assuming you have a Visit model
            image_file = req.FILES['image']
            print("Received image file:", image_file.name)  # Print the name of the received file
            curr_obj.signature = image_file  # Assuming you have a signature field in your Visit model
            curr_obj.save()
            return JsonResponse({'success': True})
        else:
            print("No 'image' field found in request.FILES")
            return JsonResponse({'success': False, 'error': 'Missing image data'})
    else:
        print("Invalid request method")
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
 
def generate_appointment_badge(req, pk):
    curr_obj = get_object_or_404(Appointment, id=pk)
    # Create QR code as before
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{curr_obj.guest}#{curr_obj.host}@{datetime.now()}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to base64 encoding
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    context= {
        'qr_code_base64': qr_code_base64,
        'curr_obj':curr_obj
        }
    
    return render(req, 'base/partials/appointment_badge.html',context)

def sign_appointment(req, pk):
    if req.method == 'POST':
        print("Received POST request to sign_visit")
        print("Request FILES:", req.FILES)  # Print request.FILES to inspect its contents
        if 'image' in req.FILES:
            curr_obj = Appointment.objects.get(id=pk)  # Assuming you have a Visit model
            image_file = req.FILES['image']
            print("Received image file:", image_file.name)  # Print the name of the received file
            curr_obj.signature = image_file  # Assuming you have a signature field in your Visit model
            curr_obj.save()
            return JsonResponse({'success': True})
        else:
            print("No 'image' field found in request.FILES")
            return JsonResponse({'success': False, 'error': 'Missing image data'})
    else:
        print("Invalid request method")
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
