from django.forms import ModelForm
from django import forms
from .models import *


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('host',
                  'guest',
                  'civility',
                  'gender',
                  'context',
                  'tel',
                  'nationality',
                  'id_doc',
                  'doc_num',)
        exclude = ('status', 'date',)
        widgets = {
            'host': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'guest': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'civility': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'context': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'gender': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'id_doc': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'doc_num': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class EditVisitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["guest"].label = 'Nom et prénoms du visiteur'
        self.fields["civility"].label = 'Civilité'
        self.fields["context"].label = 'Context de la visite'
        self.fields["tel"].label = 'Téléphone'
        self.fields["nationality"].label = 'Nationalité'
        self.fields["arrived_at"].label = "Heure d'arrivée"
        self.fields["departed_at"].label = 'Heure de départ'
        self.fields["gender"].label = 'Sexe'
        self.fields["id_doc"].label = "Pièce d'identité"
        self.fields["doc_num"].label = "N° de la pièce d'identité"
        self.fields["status"].label = 'Status de la visite'

    class Meta:
        model = Visit
        fields = ('__all__')
        exclude = ('host', 'date',)
        widgets = {
            'host': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'civility': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'guest': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'gender': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'context': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'arrived_at': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'departed_at': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'id_doc': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'doc_num': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'status': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('guest',
                  'civility',
                  'gender',
                  'tel',
                  'date',
                  'time',
                  'is_vip',)
        exclude = ('status', )
        widgets = {
            'host': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'guest': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'civility': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'gender': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'time': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'is_vip': forms.CheckboxInput(),


        }


class EditAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["guest"].label = 'Nom et prénoms du visiteur'
        self.fields["civility"].label = 'Civilité'
        self.fields["gender"].label = 'Sexe'
        self.fields["nationality"].label = 'Nationalité'
        self.fields["tel"].label = 'Téléphone'
        self.fields["time"].label = 'Heure du Rendez-vous'
        self.fields["arrived_at"].label = "Heure d'arrivée"
        self.fields["departed_at"].label = 'Heure de départ'
        self.fields["id_doc"].label = "Pièce d'identité"
        self.fields["doc_num"].label = "N° de la pièce d'identité"
        self.fields["status"].label = 'Status du Rendez-vous'
        self.fields["is_vip"].label = 'Rendez-vous V.I.P'

    class Meta:
        model = Appointment
        fields = ('__all__')
        exclude = ('host',)
        widgets = {
            'guest': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'gender': forms.Select(attrs={'class': "mb-2 px-6 py-2 rounded-md bg-white w-full"}),
            'civility': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'time': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'arrived_at': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'departed_at': TimeInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'id_doc': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'doc_num': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'status': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'is_vip': forms.CheckboxInput(),
        }
