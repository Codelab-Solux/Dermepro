from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from base.utils import h_encode, h_decode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from chats.models import ChatMessage

from datetime import date

# Create your models here.
civility_types = (('M.', 'Monsieur'),
                  ('Mme.', "Madame"),
                  ('Mlle.', "Mademoiselle"),
                  )

visit_types = (('friendly', 'Amicale'),
               ('familial', 'Familiale'),
               ('professional', "Professionelle"),)

genders = (
        ('female', "Feminin"),
    ('male', 'Masculin'),
        )
id_types = (
    ('id_card', "Carte d'identité"),
    ('vote_card', "Carte d'électeur"),
    ('drv_license', "Permit de conduire"),
    ('passport', "Passport international"),
)


class Status(models.Model):
    title = models.CharField(max_length = 255)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('status', kwargs={'pk': self.pk})


class Visit(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    guest = models.CharField(max_length=255)
    civility = models.CharField(max_length=50, blank=True,
                                null=True, choices=civility_types, default='')
    context = models.CharField(max_length=50, blank=True,
                               null=True, choices=visit_types, default='professionelle')
    tel = models.IntegerField(default='', null=True, blank=True)
    nationality = models.CharField(
        max_length=255, default='', null=True, blank=True)
    date = models.DateField(default=date.today)
    arrived_at = models.TimeField(blank=True, null=True)
    accepted_at = models.TimeField(blank=True, null=True)
    departed_at = models.TimeField(null=True, blank=True)
    sex = models.CharField(max_length=50, blank=True,
                              null=True, choices=genders, default='')
    id_doc = models.CharField(max_length=50, blank=True,
                              null=True, choices=id_types, default='')
    doc_num = models.IntegerField(blank=True, null=True, default='')
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    # signature = models.TextField(null=True, blank=True)

    # def set_signature(self, data):
    #     self.signature = json.dumps(data)

    # def get_signature(self):
    #     return json.loads(self.signature) if self.signature else None
    
    def __str__(self):
        return self.guest

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('visit', kwargs={'pk': self.pk})


class Appointment(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    guest = models.CharField(max_length=255)
    civility = models.CharField(max_length=50, blank=True,
                                null=True, choices=civility_types, default='')
    tel = models.CharField(max_length=128, default='', null=True, blank=True)
    nationality = models.CharField(
        max_length=255, default='', null=True, blank=True)
    date = models.DateField(default=date.today)
    time = models.TimeField(null=True, blank=True)
    arrived_at = models.TimeField(null=True, blank=True)
    departed_at = models.TimeField(null=True, blank=True)
    sex = models.CharField(max_length=50, blank=True,
                              null=True, choices=genders, default='')
    id_doc = models.CharField(max_length=50, blank=True,
                              null=True, choices=id_types, default='')
    doc_num = models.CharField(
        max_length=50, blank=True, null=True, default='')
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    # signature = models.TextField(null=True, blank=True)

    # def set_signature(self, data):
    #     self.signature = json.dumps(data)

    # def get_signature(self):
    #     return json.loads(self.signature) if self.signature else None
    # def __str__(self):
    #     return self.guest

    def __str__(self):
        return self.guest

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('appointment', kwargs={'pk': self.pk})


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Notification for < user: {self.user.username}>'

    def get_hashid(self):
        return h_encode(self.id)
