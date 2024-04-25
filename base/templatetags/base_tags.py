from django import template
from django.shortcuts import get_object_or_404
from base.models import *
from accounts.models import *
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
def get_hour_schedule(objects, day, hour):
    # Filter appointments for the given day and hour
    day_appointments = objects.filter(date=day)
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
def by_time(objects, hour):
    return objects.filter(time__hour=hour)


@register.filter(name='by_day')
def by_day(objects, day_name):
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
    desired_day = current_date - \
        timedelta(days=current_date.weekday() - day_number)

    # Filter appointments for the desired day
    return objects.filter(date=desired_day)


@register.filter(name='by_ref_date')
def by_ref_date(objects, ref_date):
    if ref_date is None:
        ref_date = datetime.now()

    desired_day = ref_date - timedelta(days=ref_date.weekday() - 0)

    return objects.filter(date=desired_day)


@register.filter(name='by_week')
def by_week(objects, week=None):
    current_date = datetime.now()

    # Calculate the date of the first day of the given week
    if week is None:
        week = current_date.isocalendar()[1]

    # Calculate the date of the first day of the given week
    first_day_of_week = current_date - \
        timedelta(weeks=current_date.isocalendar()[
                  1] - week, days=current_date.weekday())

    # Filter appointments for the desired week
    return objects.filter(date__gte=first_day_of_week, date__lt=first_day_of_week + timedelta(days=7))


@register.filter(name='by_year')
def by_year(objects, year=None):
    current_date = datetime.now()

    # Calculate the date of the first day of the given year
    if year is None:
        year = current_date.year
    first_day_of_year = datetime(year, 1, 1)

    # Filter appointments for the desired year
    return objects.filter(date__gte=first_day_of_year, date__lt=datetime(year + 1, 1, 1))


@register.filter
def get_visit_count(pk):
    user = CustomUser.objects.get(id=pk)
    visit_count = int(Visit.objects.filter(host=user).count())
    return visit_count


@register.filter
def get_visit_duration(pk):
    visit = Visit.objects.get(id=pk)

    if visit.is_accepted and visit.status.id == 3:
        start_time = visit.started_at
        end_time = visit.departed_at

        # Use some fixed date for conversion (e.g., today's date)
        fixed_date = datetime.today().date()

        # Convert TimeField values to datetime objects with fixed date
        accepted_datetime = datetime.combine(fixed_date, start_time)
        departed_datetime = datetime.combine(fixed_date, end_time)

        # Calculate the duration in seconds
        duration_seconds = (departed_datetime -
                            accepted_datetime).total_seconds()

        # Calculate days, hours, and minutes
        # 86400 seconds in a day
        days, remainder = divmod(duration_seconds, 86400)
        # 3600 seconds in an hour
        hours, remainder = divmod(remainder, 3600)
        # 60 seconds in a minute
        minutes, seconds = divmod(remainder, 60)

        duration = {
            'days': int(days),
            'hours': int(hours),
            'minutes': int(minutes),
        }
    else:
        duration = {
            'days': 0,
            'hours': 0,
            'minutes': 0,
        }

    return duration


@register.filter
def get_total_visit_time(pk):
    user = get_object_or_404(CustomUser, id=pk)
    total_time = timedelta()

    # Iterate over all visits of the user
    for obj in Visit.objects.filter(host=user):
        duration = get_visit_duration(obj.pk)
        duration_timedelta = timedelta(
            days=duration['days'], hours=duration['hours'], minutes=duration['minutes'])
        total_time += duration_timedelta

        # Extract days, hours, and minutes from total duration
    total_days = total_time.days
    total_hours, remainder_minutes = divmod(total_time.seconds, 3600)
    total_minutes = remainder_minutes // 60

    total_time = {
        'days': total_days,
        'hours': total_hours,
        'minutes': total_minutes
    }

    return total_time


def get_total_visits_minutes(user):
    total_time = timedelta()

    # Iterate over all appointments of the user
    for visit in Visit.objects.filter(host=user):
        duration = get_visit_duration(visit.pk)
        duration_minutes = (duration['days'] * 24 * 60) + \
            (duration['hours'] * 60) + duration['minutes']
        total_time += timedelta(minutes=duration_minutes)

    return total_time.total_seconds() // 60  # Convert total time to minutes

@register.filter
def get_appt_count(pk):
    user = CustomUser.objects.get(id=pk)
    appt_count = int(Appointment.objects.filter(host=user).count())
    return appt_count


@register.filter
def get_appt_duration(pk):
    appt = Appointment.objects.get(id=pk)

    if appt.status.id == 3:
        start_time = appt.started_at
        end_time = appt.ended_at

        # Use some fixed date for conversion (e.g., today's date)
        fixed_date = datetime.today().date()

        # Convert TimeField values to datetime objects with fixed date
        accepted_datetime = datetime.combine(fixed_date, start_time)
        departed_datetime = datetime.combine(fixed_date, end_time)

        # Calculate the duration in seconds
        duration_seconds = (departed_datetime -
                            accepted_datetime).total_seconds()

        # Calculate days, hours, and minutes
        # 86400 seconds in a day
        days, remainder = divmod(duration_seconds, 86400)
        # 3600 seconds in an hour
        hours, remainder = divmod(remainder, 3600)
        # 60 seconds in a minute
        minutes, seconds = divmod(remainder, 60)

        duration = {
            'days': int(days),
            'hours': int(hours),
            'minutes': int(minutes),
        }
    else:
        duration = {
            'days': 0,
            'hours': 0,
            'minutes': 0,
        }

    return duration


@register.filter
def get_total_appt_time(pk):
    user = get_object_or_404(CustomUser, id=pk)
    total_time = timedelta()

    # Iterate over all visits of the user
    for obj in Appointment.objects.filter(host=user):
        duration = get_appt_duration(obj.pk)
        duration_timedelta = timedelta(
            days=duration['days'], hours=duration['hours'], minutes=duration['minutes'])
        total_time += duration_timedelta

        # Extract days, hours, and minutes from total duration
    total_days = total_time.days
    total_hours, remainder_minutes = divmod(total_time.seconds, 3600)
    total_minutes = remainder_minutes // 60

    total_time = {
        'days': total_days,
        'hours': total_hours,
        'minutes': total_minutes
    }

    return total_time


@register.filter
def get_total_appointment_minutes(user):
    total_time = timedelta()

    # Iterate over all appointments of the user
    for appointment in Appointment.objects.filter(host=user):
        duration = get_appt_duration(appointment.pk)
        duration_minutes = (duration['days'] * 24 * 60) + \
            (duration['hours'] * 60) + duration['minutes']
        total_time += timedelta(minutes=duration_minutes)

    return total_time.total_seconds() // 60  #


