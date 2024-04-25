from django.db import models
from django.urls import reverse
from accounts.models import CustomUser, Profile
from datetime import date
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from base.utils import h_encode, h_decode
from django.template.loader import get_template


context_types = (('friendly', 'Amicale'),
                 ('familial', 'Familiale'),
                 ('professional', "Professionelle"),)

genders = (('female', "Feminin"), ('male', 'Masculin'),)

id_types = (
    ('id_card', "Carte Nationale d'Identité (CNI)"),
    ('consul_card', "Carte Consulaire"),
    ('ecowas_card', "Carte CEDEAO"),
    ('driver_license', "Permit de conduire"),
    ('passport', "Passport international"),
)

company_types = (
    ('SC', "SC"),
    ('SA', "SA"),
    ('SAS', "SAS"),
    ('SNS', "SNS"),
    ('SNC', "SNC"),
    ('SANC', "SANC"),
    ('SARL', "SARL"),
    ('SARLU', "SARLU"),
)


class WorkDay(models.Model):
    name = models.CharField(max_length=255)
    fr_name = models.CharField(max_length=255)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.fr_name

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('workday', kwargs={'pk': self.pk})


class Status(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('status', kwargs={'pk': self.pk})


class Visit(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=50, choices=genders)
    phone = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    context = models.CharField(max_length=50, choices=context_types)
    nationality = models.CharField(
        max_length=255, default='', null=True, blank=True)
    date = models.DateField(default=date.today)
    arrived_at = models.TimeField(default=timezone.now)
    started_at = models.TimeField(blank=True, null=True)
    ended_at = models.TimeField(blank=True, null=True)
    departed_at = models.TimeField(null=True, blank=True)
    id_document = models.CharField(max_length=50, choices=id_types)
    id_number = models.CharField(max_length=50)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_missed = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    signature = models.ImageField(
        upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} - {self.first_name}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('visit', kwargs={'pk': self.pk})


class Appointment(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=50, choices=genders)
    context = models.CharField(
        max_length=50, choices=context_types, default='professional')
    nationality = models.CharField(
        max_length=255, default='', null=True, blank=True)
    date = models.DateField(default=date.today)
    time = models.TimeField()
    started_at = models.TimeField(default=timezone.now)
    ended_at = models.TimeField(null=True, blank=True)
    departed_at = models.TimeField(null=True, blank=True)
    id_document = models.CharField(
        max_length=50, choices=id_types, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_missed = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    signature = models.ImageField(
        upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} - {self.first_name}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('appointment', kwargs={'pk': self.pk})


class Company(models.Model):
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    company_type = models.CharField(max_length=50, choices=company_types)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    employees = models.ManyToManyField(
        Profile, related_name='companies', blank=True)
    workdays = models.ManyToManyField(WorkDay, blank=True)
    is_verified = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.company_type}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('Companies', kwargs={'pk': self.pk})


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    notice = models.CharField(
        max_length=255, default='', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for user: {self.user.username}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_notification_html(self):
        template = get_template('base/components/notification_card.html')
        rendered_html = template.render({'obj': self})
        return rendered_html
