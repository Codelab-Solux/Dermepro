from django import template
from django.shortcuts import get_object_or_404
from base.models import *
from accounts.models import Profile
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SU
register = template.Library()

@register.filter
def get_model_name(obj):
    return obj._meta.model_name

def get_week_boundaries(year, week):
    # Get the first day of the week (Monday) for the given ISO year and week
    first_day_of_week = datetime.fromisocalendar(year, week, 1)
    
    # Get the last day of the week (Sunday) for the given ISO year and week
    last_day_of_week = first_day_of_week + relativedelta(weekday=SU)
    
    return first_day_of_week.date(), last_day_of_week.date()


@register.filter
def get_hour_schedule(appts, day, hour):
    # Filter appointments for the given day and hour
    day_appointments = appts.filter(date=day)
    # Extract the hour from the datetime objects and filter again
    hour_appointments = day_appointments.filter(time__hour=hour)
    return hour_appointments


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_day_one(curr_date):
    return curr_date - timedelta(days=curr_date.weekday())


@register.filter
def add_days(date, days):
    return date + timedelta(days=days)



@register.filter(name='by_time')
def by_time(appts, hour):
    return appts.filter(time__hour=hour)


@register.filter(name='by_day')
def by_day(appts, day_name):
    current_date = datetime.now()

    # Calculate the date of the specified day
    days_mapping = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    # Validate day_name
    if day_name.lower() not in days_mapping:
        raise ValueError(f"Invalid day name: {day_name}")

    day_number = days_mapping[day_name.lower()]
    desired_day = current_date - timedelta(days=current_date.weekday() - day_number)

    # Filter appointments for the desired day
    return appts.filter(date=desired_day)


@register.filter(name='by_ref_date')
def by_ref_date(appts, ref_date):
    if ref_date is None:
        ref_date = datetime.now()

    desired_day = ref_date - timedelta(days=ref_date.weekday() - 0)

    return appts.filter(date=desired_day)


@register.filter(name='by_week')
def by_week(appts, week=None):
    current_date = datetime.now()

    # Calculate the date of the first day of the given week
    if week is None:
        week = current_date.isocalendar()[1]

    # Calculate the date of the first day of the given week
    first_day_of_week = current_date - timedelta(weeks=current_date.isocalendar()[1] - week, days=current_date.weekday())

    # Filter appointments for the desired week
    return appts.filter(date__gte=first_day_of_week, date__lt=first_day_of_week + timedelta(days=7))


@register.filter(name='by_year')
def by_year(appts, year=None):
    current_date = datetime.now()

    # Calculate the date of the first day of the given year
    if year is None:
        year = current_date.year
    first_day_of_year = datetime(year, 1, 1)

    # Filter appointments for the desired year
    return appts.filter(date__gte=first_day_of_year, date__lt=datetime(year + 1, 1, 1))


@register.filter
def get_visit_count(pk):
    user = CustomUser.objects.get(id=pk)
    visit_count = int(Visit.objects.filter(host=user).count())
    return visit_count

@register.filter
def get_appt_count(pk):
    user = CustomUser.objects.get(id=pk)
    appt_count = int(Appointment.objects.filter(host=user).count())
    return appt_count
