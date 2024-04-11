import json
import calendar
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.db.models.query import QuerySet
from accounts.forms import RoleForm
from accounts.models import *
from .models import *
from .forms import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import csv
import qrcode
import base64
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SU
from calendar import Calendar, month_name, monthrange
from django.core.serializers import serialize
from collections import defaultdict
from .templatetags.base_tags import get_hour_schedule


def get_week_boundaries(year, week):
    # Get the first day of the week (Monday) for the given ISO year and week
    first_day_of_week = datetime.fromisocalendar(year, week, 1)

    # Get the last day of the week (Sunday) for the given ISO year and week
    last_day_of_week = first_day_of_week + relativedelta(weekday=SU)

    return first_day_of_week.date(), last_day_of_week.date()


def get_curr_week_number():
    # Get today's date
    today = date.today()

    # Get the ISO week number
    _, week_number, _ = today.isocalendar()

    return week_number


def get_month_from_week(year, week_number):
    # Create a datetime object for the first day of the given year
    first_day_of_year = datetime(year, 1, 1)

    # Calculate the date of the first day of the given week
    first_day_of_week = first_day_of_year + timedelta(weeks=week_number - 1)

    # Get the month from the first day of the week
    month = first_day_of_week.month

    return month


def get_date_from_day_number(year, day):
    first_day_of_year = datetime(year, 1, 1)
    set_day = first_day_of_year + timedelta(days=day - 1)
    date = set_day.date()
    return date


def paginate_objects(req, obj_list, obj_count=10):
    paginator = Paginator(obj_list, obj_count)
    page_number = req.GET.get('page', 1)
    objects = paginator.get_page(page_number)
    return objects


@login_required(login_url='login')
def home(req):
    user = req.user
    today = datetime.today()
    day = today.timetuple().tm_yday
    week = today.isocalendar()[1]
    year = today.year

    context = {
        "home_page": "active",
        'title': 'Home',
        'day': day,
        'week': week,
        'year': year,
    }
    return render(req, 'base/index.html', context)


# visits -------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def visits(req):
    user = req.user
    statuses = Status.objects.all()
    hosts = CustomUser.objects.all()
    if user.role.sec_level >= 4:
        visits = Visit.objects.all().order_by('-date', '-arrived_at')
    else:
        visits = Visit.objects.filter(
            host=user).order_by('-date', '-arrived_at')
    context = {
        "visits_page": "active",
        'title': 'Visits',
        'visits': visits,
        'statuses': statuses,
        "hosts": hosts,
    }
    return render(req, 'base/visits.html', context)


@login_required(login_url='login')
def visit(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Visit, id=pk)

    # Mark associated notifications as read
    associated_notifications = Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(Visit), object_id=curr_obj.id)
    if associated_notifications:
        associated_notifications.update(is_read=True)
        # print(f'Notification was read at {timezone.now()}')

    context = {
        "visit_details_page": "active",
        'title': 'Visit Details',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/visit.html', context)


@login_required(login_url='login')
def visit_alt(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Visit, id=pk)

    context = {
        "visit_details_page": "active",
        'title': 'Visit Details',
        'curr_obj': curr_obj,
    }
    return render(req, 'base/visit_alt.html', context)


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
        return render(req, 'base/forms/visit_form.html', context={'form': form, 'form_title': 'Nouvelle Visite'})


@login_required(login_url='login')
def edit_visit(req, pk):
    user = req.user
    if user.role.sec_level < 4:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

    curr_obj = get_object_or_404(Visit, id=pk)

    form = VisitForm(instance=curr_obj)
    if req.method == 'POST':
        form = VisitForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/basic_form.html', context={'form': form, 'form_title': 'Modifier Une Visite', 'curr_obj': curr_obj})


@login_required(login_url='login')
def moderate_visit(req, pk, kp):
    user = req.user
    curr_obj = get_object_or_404(Visit, id=pk)
    new_status = get_object_or_404(Status, id=kp)
    host_profile = get_object_or_404(Profile, user=curr_obj.host)

    if kp == 2:
        curr_obj.is_accepted = True
        curr_obj.is_rejected = False
        curr_obj.accepted_at = timezone.now()
        curr_obj.status = new_status
        curr_obj.save()

        new_user_status = get_object_or_404(UserStatus, id=2)
        host_profile.status = new_user_status
        host_profile.save()
        # print(host_profile.status)

    elif kp == 3:
        curr_obj.is_accepted = True
        curr_obj.is_rejected = False
        curr_obj.departed_at = timezone.now()
        curr_obj.status = new_status
        curr_obj.save()

        new_user_status = get_object_or_404(UserStatus, id=1)
        host_profile.status = new_user_status
        host_profile.save()
        # print(curr_profile.status)

    elif kp == 5:
        curr_obj.is_rejected = True
        curr_obj.is_accepted = False
        curr_obj.status = new_status
        curr_obj.save()
    else:
        return "error"

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


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

    if kp == 2:
        curr_obj.is_accepted = timezone.now()
        curr_obj.save()
        new_user_status = get_object_or_404(UserStatus, id=kp)
        curr_profile.status = new_user_status
        curr_profile.save()

    else:
        new_user_status = get_object_or_404(UserStatus, id=1)
        curr_profile.status = new_user_status
        curr_profile.save()

    context = {'obj': curr_obj}
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    # return render(req, 'base/components/status_badge.html', context)


@login_required(login_url='login')
# secures the delete route and makes it only accessible by the DELETE method
@require_http_methods(['DELETE'])
def delete_visit(req, pk):
    curr_obj = get_object_or_404(Visit, id=pk)
    if req.user.role.sec_level < 4:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    success = 'Deleted successfully'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

# -----------------------visits htmx partials-----------------------


@login_required(login_url='login')
def visit_list(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.all().order_by('-date', '-arrived_at')
    else:
        visits = Visit.objects.filter(
            host=user).order_by('-date', '-arrived_at')
    context = {"visits": visits}
    return render(req, 'base/partials/visit_list.html', context)


@login_required(login_url='login')
def ongoing_visits(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.filter(
            status=2).order_by('-date', '-arrived_at')
    else:
        visits = Visit.objects.filter(
            status=2, host=user).order_by('-date', '-arrived_at')
    context = {"visits": visits}
    return render(req, 'base/partials/ongoing_visits.html', context)


@login_required(login_url='login')
def pending_visits(req):
    user = req.user
    if user.role.sec_level >= 4:
        visits = Visit.objects.filter(
            status=1).order_by('-date', '-arrived_at')
    else:
        visits = Visit.objects.filter(
            status=1, host=user).order_by('-date', '-arrived_at')
    context = {"visits": visits}
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
            base_query = base_query.filter(
                host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    if name_query:
        base_query = base_query.filter(first_name__icontains=name_query)
    if status_query:
        base_query = base_query.filter(status__id=status_query)
    if type_query:
        base_query = base_query.filter(context=type_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)

    visits = base_query

    context = {"visits": visits}
    return render(req, 'base/partials/visit_list.html', context)


def generate_visit_badge(req, pk):
    curr_obj = get_object_or_404(Visit, id=pk)
    # Create QR code as before
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{curr_obj.first_name}#{curr_obj.host}@{datetime.now()}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert image to base64 encoding
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    context = {
        'qr_code_base64': qr_code_base64,
        'curr_obj': curr_obj
    }

    return render(req, 'base/partials/visitor_badge.html', context)


def sign_visit(req, pk):
    if req.method == 'POST':
        # print("req FILES:", req.FILES)
        if 'image' in req.FILES:
            curr_obj = Visit.objects.get(id=pk)
            image_file = req.FILES['image']
            # print("Received image file:", image_file.name)
            curr_obj.signature = image_file
            curr_obj.departed_at = timezone.now()
            curr_obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            # print("No 'image' field found in req.FILES")
            return JsonResponse({'success': False, 'error': 'Missing image data'})
    else:
        # print("Invalid req method")
        return JsonResponse({'success': False, 'error': 'Invalid req method'})


@ login_required(login_url='login')
def visit_status(req, pk):
    curr_obj = get_object_or_404(Visit, id=pk)
    context = {"curr_obj": curr_obj}
    return render(req, 'base/partials/visit_status.html', context)


# appointments -------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def appointments(req):
    user = req.user
    curr_date = datetime.today()
    curr_week = curr_date.isocalendar()[1]
    hosts = CustomUser.objects.all()
    statuses = Status.objects.all()

    context = {
        "rdvs_page": "active",
        'title': 'Appointments Calendar',
        'curr_date': curr_date,
        'curr_week': curr_week,
        'hosts': hosts,
        'statuses': statuses,
    }

    return render(req, 'base/appointments.html', context)


@login_required(login_url='login')
def calendar_week(req, week=None):
    user = req.user

    if not week:
        week = datetime.today().isocalendar()[1]

    # print(f'Weeeeeeeeeeeeeeeeeeeeeeeeeeek : {week}')

    year = datetime.today().year
    month = get_month_from_week(year, week)
    month_name = calendar.month_name[month]
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Mapping dictionary from English to French day names
    day_mapping = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        # 'Sunday': 'Dimanche'
    }
    curr_company = Company.objects.first()
    starts_at = curr_company.opening_time.hour
    ends_at = curr_company.closing_time.hour
    if not starts_at:
        starts_at = 8
    if not ends_at:
        ends_at = 18

    hours = list(range(starts_at, ends_at + 1))
        
    first_day_of_week, last_day_of_week = get_week_boundaries(year, week)
    if user.role.sec_level >= 4:
        appointments = Appointment.objects.filter(
            date__range=(first_day_of_week, last_day_of_week)
        ).order_by('-date', '-time')
    else:
        appointments = Appointment.objects.filter(
            date__range=(first_day_of_week, last_day_of_week), host=user
        ).order_by('-date', '-time')

    # print(f'appointments : {appointments}')
    workdays = WorkDay.objects.filter(company = curr_company)
    
    context = {
        "rdv_calendar": "active",
        'title': 'Appointments Calendar',
        'week': week,
        'workdays': workdays,
        'year': year,
        'month': month,
        'month_name': month_name,
        'day_one': first_day_of_week,
        'hours': hours,
        'appts': appointments,
    }

    return render(req, 'base/partials/calendar_week.html', context)


@login_required(login_url='login')
def calendar_day(req, day=None):
    user = req.user
    if day:
        curr_date = get_date_from_day_number(datetime.today().year, day)
    else:
        curr_date = datetime.today()

    week = curr_date.isocalendar()[1]
    month = curr_date.month
    year = curr_date.year
    month = get_month_from_week(year, week)
    month_name = calendar.month_name[month]

    curr_company = Company.objects.first()
    starts_at = curr_company.opening_time.hour
    ends_at = curr_company.closing_time.hour
    if not starts_at:
        starts_at = 8
    if not ends_at:
        ends_at = 18

    hours = list(range(starts_at, ends_at + 1))

    if user.role.sec_level >= 4:
        appointments = Appointment.objects.filter(
            date=curr_date).order_by('-time')
    else:
        appointments = Appointment.objects.filter(
            date=curr_date, host=user).order_by('-time')

    context = {
        "rdv_calendar": "active",
        'title': 'Appointments Calendar',
        'day': day,
        'curr_date': curr_date,
        'week': week,
        'year': year,
        'month': month,
        'month_name': month_name,
        'hours': hours,
        'appts': appointments,
    }

    return render(req, 'base/partials/calendar_day.html', context)


@ login_required(login_url='login')
def appointment(req, pk):
    user = req.user
    curr_obj = Appointment.objects.get(id=pk)

    # Mark associated notifications as read
    associated_notifications = Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(Appointment), object_id=curr_obj.id)
    if associated_notifications:
        associated_notifications.update(is_read=True)
        # print(f'Notification was read at {timezone.now()}')

    context = {
        "appointment_details_page": "active",
        'title': 'Appointment Details',
        'curr_obj': curr_obj,

    }
    return render(req, 'base/appointment.html', context)


@ login_required(login_url='login')
def appointment_alt(req, pk):
    user = req.user
    curr_obj = Appointment.objects.get(id=pk)

    context = {
        "appointment_details_page": "active",
        'title': 'Appointment Details',
        'curr_obj': curr_obj,

    }
    return render(req, 'base/appointment_alt.html', context)


@login_required(login_url='login')
def create_appointment(req):
    user = req.user
    if user.role.sec_level < 4:
        return redirect('home')

    form = AppointmentCreateForm()
    if req.method == 'POST':
        form = AppointmentCreateForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success = 'Nouveau rendez-vous ajouté'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/appointment_form.html', context={'form': form, 'form_title': 'Nouveau Rendez-vous'})


@login_required(login_url='login')
def edit_appointment(req, pk):
    user = req.user
    # if user.role.sec_level < 4:
    #     return redirect('visits')

    curr_obj = get_object_or_404(Appointment, id=pk)

    form = AppointmentEditForm(instance=curr_obj)
    if req.method == 'POST':
        form = AppointmentEditForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/basic_form.html', context={'form': form, 'form_title': 'Modifier  Ce Rendez-vous', 'curr_obj': curr_obj})


@login_required(login_url='login')
def moderate_appointment(req, pk, kp):
    user = req.user
    curr_obj = get_object_or_404(Appointment, id=pk)
    host_profile = get_object_or_404(Profile, user=curr_obj.host)
    new_status = get_object_or_404(Status, id=kp)

    # starts the appointment
    if kp == 2:
        curr_obj.started_at = timezone.now()
        curr_obj.status = new_status
        curr_obj.save()
        new_user_status = get_object_or_404(UserStatus, id=2)
        host_profile.status = new_user_status
        host_profile.save()

    # ends the appointment

    elif kp == 3:
        curr_obj.ended_at = timezone.now()
        curr_obj.departed_at = timezone.now()
        curr_obj.status = new_status
        curr_obj.save()
        # ---------------------------------------------------
        new_user_status = get_object_or_404(UserStatus, id=1)
        host_profile.status = new_user_status
        host_profile.save()

    else:
        return "error"

    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def edit_appointment_status(req, pk, kp):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    curr_obj = get_object_or_404(Appointment, id=pk)
    new_status = get_object_or_404(Status, id=kp)
    curr_obj.status = new_status
    curr_obj.save()

    if kp == 2:
        new_user_status = get_object_or_404(UserStatus, id=kp)
        curr_profile.status = new_user_status
        curr_profile.save()

    else:
        new_user_status = get_object_or_404(UserStatus, id=1)
        curr_profile.status = new_user_status
        curr_profile.save()
        # print(curr_profile.status)

    context = {'obj': curr_obj}
    return render(req, 'base/components/status_badge.html', context)


@login_required(login_url='login')
# secures the delete route and makes it only accessible by the DELETE method
@require_http_methods(['DELETE'])
def delete_appointment(req, pk):
    curr_obj = get_object_or_404(Appointment, id=pk)
    if req.user.role.sec_level < 5:
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    curr_obj.delete()
    success = 'Deleted successfully'
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})

# ---------------------appointments htmx partials-----------------------


@login_required(login_url='login')
def appointment_list(req):
    user = req.user
    if user.role.sec_level >= 4:
        appointments = Appointment.objects.all().order_by('-date', '-time')
    else:
        appointments = Appointment.objects.filter(
            host=user).order_by('-date', '-time')
    context = {"appointments": appointments}
    return render(req, 'base/partials/appointment_list.html', context)


@login_required(login_url='login')
def appointment_grid(req):
    user = req.user
    if user.role.sec_level >= 4:
        appointments = Appointment.objects.all().order_by('-date', '-time')
    else:
        appointments = Appointment.objects.filter(
            host=user).order_by('-date', '-time')
    context = {"appointments": appointments}
    return render(req, 'base/partials/appointment_grid.html', context)


@login_required(login_url='login')
def pending_vips(req):
    appointments = Appointment.objects.filter(is_vip=True, status=1)
    context = {"appointments": appointments}
    return render(req, 'base/partials/pending_vips.html', context)


@login_required(login_url='login')
def pending_appointments(req):
    appointments = Appointment.objects.filter(status=1).exclude(is_vip=True)
    context = {"appointments": appointments}
    return render(req, 'base/partials/pending_appointments.html', context)

@login_required(login_url='login')
def pending_appointments_all(req):
    appointments = Appointment.objects.filter(status=1)
    context = {"appointments": appointments}
    return render(req, 'base/partials/pending_appointments_all.html', context)


@login_required(login_url='login')
def ongoing_appointments(req):
    appointments = Appointment.objects.filter(status=2)
    context = {"appointments": appointments}
    return render(req, 'base/partials/ongoing_appointments.html', context)


def filter_appointments(req, pk='list'):
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
            base_query = base_query.filter(
                host__username__icontains=host_query)
    else:
        base_query = base_query.filter(host=user)

    if name_query:
        base_query = base_query.filter(first_name__icontains=name_query)
    if status_query:
        base_query = base_query.filter(status__id=status_query)
    if sex_query:
        base_query = base_query.filter(sex=sex_query)

    appointments = base_query
    context = {"appointments": appointments}
    print(appointments)
    if pk == 'grid':
        return render(req, 'base/partials/appointment_grid.html', context)
    else:
        return render(req, 'base/partials/appointment_list.html', context)


def generate_appointment_badge(req, pk):
    curr_obj = get_object_or_404(Appointment, id=pk)
    # Create QR code as before
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{curr_obj.first_name}#{curr_obj.host}@{datetime.now()}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert image to base64 encoding
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    context = {
        'qr_code_base64': qr_code_base64,
        'curr_obj': curr_obj
    }

    return render(req, 'base/partials/appointment_badge.html', context)


def sign_appointment(req, pk):
    if req.method == 'POST':
        # print("req FILES:", req.FILES)
        if 'image' in req.FILES:
            curr_obj = Appointment.objects.get(id=pk)
            image_file = req.FILES['image']
            # print("Received image file:", image_file.name)
            curr_obj.signature = image_file
            curr_obj.departed_at = timezone.now()
            curr_obj.save()
            return JsonResponse({'success': True})
        else:
            # print("No 'image' field found in req.FILES")
            return JsonResponse({'success': False, 'error': 'Missing image data'})
    else:
        # print("Invalid req method")
        return JsonResponse({'success': False, 'error': 'Invalid req method'})


@ login_required(login_url='login')
def appointment_status(req, pk):
    curr_obj = get_object_or_404(Appointment, id=pk)
    context = {"curr_obj": curr_obj}
    return render(req, 'base/partials/appointment_status.html', context)


# parameters -------------------------------------------------------------------------------------------------
@ login_required(login_url='login')
def parameters(req):
    user = req.user
    if user.role.sec_level < 3:
        curr_comp = get_object_or_404(Company, id=user.profile.company.id)
    else:
        curr_comp = get_object_or_404(Company, manager=user)

    users = CustomUser.objects.all()
    user_roles = Role.objects.all()
    first_day = curr_comp.workdays.first()
    last_day = curr_comp.workdays.last()

    form = RoleForm()
    if req.method == 'POST':
        form = RoleForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('parameters')

    context = {
        "params_page": "active",
        'title': 'Parameters',
        'users': users,
        'user_roles': user_roles,
        'curr_comp': curr_comp,
        'first_day': first_day,
        'last_day': last_day ,
        'form': form,
    }
    return render(req, 'base/parameters.html', context)


@login_required(login_url='login')
def edit_company(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Company, id=pk, manager=user)

    form = CompanyForm(instance=curr_obj)
    if req.method == 'POST':
        form = CompanyForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success = 'Données modifiée avec success'
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/forms/company_form.html', context={'form': form, 'form_title': 'Modifier Cette Compagnie', 'curr_obj': curr_obj})


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


# reports -------------------------------------------------------------------------------------------------
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

# -----------------------users report partials-----------------------


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

# -----------------------visits report partials-----------------------


def visits_table(req):
    user = req.user
    visits = Visit.objects.all().order_by('-date', '-arrived_at')
    objects = paginate_objects(req, visits)
    context = {'objects': objects}
    return render(req, 'base/partials/visits_table.html', context)
    # return render(req, 'base/reports.html', context)


def filter_visits_table(req):
    user = req.user
    # Get filter parameters from req
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
            base_query = base_query.filter(
                host__username__icontains=host_query)
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

    # If the req is for CSV export, generate and return CSV response
    if req.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="visites.csv"'
        writer = csv.writer(response)

        # Write header row
        writer.writerow(['Date', 'Hôte', 'Visiteur', 'phoneephone', 'Sexe', 'Cadre',
                        "Heure d'arrivée", "Heure de debut", "Heure de départ", "Status"])

        # Write data rows
        for visit in visits:
            writer.writerow([visit.date, visit.host.username, visit.first_name, visit.phone, visit.sex,
                            visit.context, visit.arrived_at, visit.accepted_at, visit.departed_at, visit.status])

        return response

    # For regular view rendering, paginate and return context
    objects = paginate_objects(req, visits)
    context = {'objects': objects}
    return render(req, 'base/partials/visits_table.html', context)

# -----------------------appointments report partials-----------------------


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
            base_query = base_query.filter(
                host__username__icontains=host_query)
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


# notifications-------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def notification_list(req):
    user = req.user
    notifications = Notification.objects.filter(user=user, is_read=False)
    context = {
        'notifications_list': 'active',
        'notifications': notifications,
    }
    return render(req, 'base/partials/notification_list.html', context)


@login_required(login_url='login')
def notifications(req):
    user = req.user
    notifications = Notification.objects.filter(user=user)
    context = {
        'notifications_page': 'active',
        'notifications': notifications,
    }
    return render(req, 'base/notifications.html', context)


@login_required(login_url='login')
def read_notification(req, pk):
    user = req.user
    curr_obj = get_object_or_404(Notification, id=pk, user=user)
    curr_obj.is_read = True
    curr_obj.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@ login_required(login_url='login')
def badge(req):
    user = req.user
    curr_profile = get_object_or_404(Profile, user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)
    context = {"curr_profile": curr_profile, 'notifications': notifications}
    return render(req, 'base/partials/badge.html', context)


# dashboard -------------------------------------------------------------------------------------------------
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
        'title': 'Dashboard',
        'appointments': appointments,
        'visits': visits,
        'users': users,
        'sex_list': sex_list,
        'visit_figs': visit_figs,
        'rdvs_stats': rdvs_stats,
    }
    return render(req, 'base/dashboard.html', context)


@ login_required(login_url='login')
def dash_overview(req):
    today = datetime.now().date()
    visits = Visit.objects.all()
    visits_json = serialize('json', visits)
    visits_count = Visit.objects.all().count()
    mal_visits = visits.filter(sex='male').count()
    fem_visits = visits.filter(sex='female').count()
    accp_visits = visits.filter(is_accepted=True).count()
    misd_visits = visits.filter(is_missed=True, status=4).count()
    cncl_visits = visits.filter(is_rejected=True, status=5).count()
    pending_visits = visits.filter(status=1, date=today).count()
    active_visits = visits.filter(status=2, date=today).count()
    finished_visits = visits.filter(status=3, date=today).count()
    # --------------------------------------------------------------
    appointments = Appointment.objects.all()
    appointments_json = serialize('json', appointments)
    appointments_count = Appointment.objects.all().count()
    mal_appointments = appointments.filter(sex='male').count()
    fem_appointments = appointments.filter(sex='female').count()
    accp_appointments = appointments.filter(is_accepted=True).count()
    misd_appointments = appointments.filter(is_missed=True, status=4).count()
    cncl_appointments = appointments.filter(
        is_cancelled=True, status=5).count()
    pending_appointments = appointments.filter(status=1, date=today).count()
    active_appointments = appointments.filter(status=2, date=today).count()
    finished_appointments = appointments.filter(status=3, date=today).count()
    # --------------------------------------------------------------
    hosts = CustomUser.objects.all()
    hosts_json = serialize('json', hosts)

    for obj in appointments:
        if obj.status.id == 3:
            obj.is_accepted = True
            obj.save()

    # print(visits_json)
    context = {
        'visits': visits,
        'visits_json': visits_json,
        'visits_count': visits_count,
        'mal_visits': mal_visits,
        'fem_visits': fem_visits,
        'accp_visits': accp_visits,
        'cncl_visits': cncl_visits,
        'misd_visits': misd_visits,
        'pending_visits': pending_visits,
        'active_visits': active_visits,
        'finished_visits': finished_visits,
        # --------------------------------
        'appointments': appointments,
        'appointments_json': appointments_json,
        'appointments_count': appointments_count,
        'mal_appointments': mal_appointments,
        'fem_appointments': fem_appointments,
        'accp_appointments': accp_appointments,
        'misd_appointments': misd_appointments,
        'cncl_appointments': cncl_appointments,
        'pending_appointments': pending_appointments,
        'active_appointments': active_appointments,
        'finished_appointments': finished_appointments,
        # --------------------------------
        'hosts_json': hosts_json,
    }

    return render(req, 'base/partials/dash_overview.html', context)


def visitor_ratio_chart(request):
    male_count = Visit.objects.filter(sex='male').count()
    female_count = Visit.objects.filter(sex='female').count()

    counts = [male_count, female_count]
    labels = ['Masculin', 'Feminin']

    context = {
        'counts': counts,
        'labels': labels,
    }

    return render(request, 'visits_by_sex.html', context)


def visitors_per_host_chart(request):
    # Assuming you have a Host model with a ForeignKey relationship with Visit
    hosts = CustomUser.objects.all()
    data = []
    for obj in hosts:
        male_visitors = Visit.objects.filter(host=obj, sex='Male').count()
        female_visitors = Visit.objects.filter(host=obj, sex='Female').count()
        data.append({
            'host_name': obj.username,
            'male_visitors': male_visitors,
            'female_visitors': female_visitors
        })
    return render(request, 'charts/visits_by_host.html', {'data': data})
