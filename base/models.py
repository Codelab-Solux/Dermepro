from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from chats.models import ChatMessage

# Create your models here.
civility_types = (('M.', 'Monsieur'),
                  ('Mme.', "Madame"),
                  ('Mlle.', "Mademoiselle"),
                  )

visit_types = (('amicale', 'Amicale'),
               ('familial', 'Familiale'),
               ('professionelle', "Professionelle"),)

gender_types = (('male', 'Masculin'),
                ('female', "Feminin"),)
id_types = (
    ('id_card', "Carte d'identité"),
    ('vote_card', "Carte d'électeur"),
    ('drv_license', "Permit de conduire"),
    ('passport', "Passport international"),
)

status_types = (
    ('pending', "En attente"),
    ('open', "En cours"),
    ('closed', "Cloturée"),
    ('ajourned', "Ajournée"),
    ('cancelled', "Annulée"),
)


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
    date = models.DateTimeField(auto_now_add=True, blank=True)
    arrived_at = models.TimeField(blank=True, null=True)
    departed_at = models.TimeField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True,
                              null=True, choices=gender_types, default='')
    id_doc = models.CharField(max_length=50, blank=True,
                              null=True, choices=id_types, default='')
    doc_num = models.IntegerField(blank=True, null=True, default='')
    status = models.CharField(max_length=50, blank=True,
                              null=True, choices=status_types, default='pending')
    # signature = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.guest

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
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    departed_at = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True,
                              null=True, choices=gender_types, default='')
    id_doc = models.CharField(max_length=50, blank=True,
                              null=True, choices=id_types, default='')
    doc_num = models.CharField(
        max_length=50, blank=True, null=True, default='')
    status = models.CharField(max_length=50, blank=True,
                              null=True, choices=status_types, default='pending')
    # signature = models.CharField(max_length=255, default='', blank=True)
    is_vip = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.guest

    def get_absolute_url(self):
        return reverse('appointment', kwargs={'pk': self.pk})


class ChatNotification(models.Model):
    chat = models.ForeignKey(to=ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Notification for < user: {self.user.username}>'
