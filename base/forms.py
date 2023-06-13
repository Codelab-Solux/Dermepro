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
        labels = {
            'host': 'Hôte',
            'guest': 'Nom et prénoms du visiteur',
            'civility': 'Civilité',
            'context': 'Context de la visite',
            'gender': 'Genre',
            'tel': 'Téléphone',
            'nationality': 'Nationalité',
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_doc': "Pièce d'identité",
            'doc_num': "N° de la pièce d'identité",
            'status': 'Status de la visite',
        }
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

    class Meta:
        model = Visit
        fields = ('__all__')
        exclude = ('date',)
        labels = {
            'host': 'Hôte',
            'guest': 'Nom et prénoms du visiteur',
            'civility': 'Civilité',
            'context': 'Context de la visite',
            'gender': 'Genre',
            'tel': 'Téléphone',
            'nationality': 'Nationalité',
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_doc': "Pièce d'identité",
            'doc_num': "N° de la pièce d'identité",
            'status': 'Status de la visite',
        }
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
        fields = ('host',
                  'guest',
                  'civility',
                  'gender',
                  'tel',
                  'date',
                  'time',
                  'is_vip',)
        exclude = ('status', )
        
        labels = {
            'host': 'Hôte',
            'guest': 'Nom et prénoms du visiteur',
            'civility': 'Civilité',
            'gender': 'Genre',
            'nationality': 'Nationalité',
            'tel': 'Téléphone',
            'time': "Heure du Rendez-vous",
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_doc': "Pièce d'identité",
            'doc_num': "N° de la pièce d'identité",
            'status': 'Status de la visite',
            'is_vip': 'Rendez-vous V.I.P',
        }
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

    class Meta:
        model = Appointment
        fields = ('__all__')
        labels = {
            'host': 'Hôte',
            'guest': 'Nom et prénoms du visiteur',
            'civility': 'Civilité',
            'gender': 'Genre',
            'nationality': 'Nationalité',
            'tel': 'Téléphone',
            'time': "Heure du Rendez-vous",
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_doc': "Pièce d'identité",
            'doc_num': "N° de la pièce d'identité",
            'status': 'Status de la visite',
            'is_vip': 'Rendez-vous V.I.P',
        }
        widgets = {
            'host': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
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
