from .models import *
from django import forms
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class VisitForm(forms.ModelForm):
    # phone = PhoneNumberField()
    class Meta:
        model = Visit
        fields = ('host',
                  'first_name',
                  'last_name',
                  'sex',
                  'context',
                  'phone',
                  'nationality',
                  'id_document',
                  'id_number',)
        exclude = ('status', 'date',)
        labels = {
            'host': 'Hôte',
            'first_name': 'Prénoms',
            'last_name': 'Nom',
            'context': 'Contexte',
            'sex': 'Sexe',
            'phone': 'Téléphone',
            'nationality': 'Nationalité',
            'departed_at': 'Heure de départ',
            'id_document': "Pièce d'identité",
            'id_number': "N° de la pièce d'identité",
            'status': 'Status de la visite',
        }
        widgets = {
            'host': forms.Select(attrs={'id': 'host_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'context': forms.Select(attrs={'id': 'context_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sex': forms.Select(attrs={'id': 'sex_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'arrived_at': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_document': forms.Select(attrs={'id': 'id_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_number': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class EditVisitForm(forms.ModelForm):
    # phone = PhoneNumberField()
    class Meta:
        model = Visit
        fields = '__all__'
        exclude = ('date',)
        labels = {
            'host': 'Hôte',
            'first_name': 'Prénoms',
            'last_name': 'Nom',
            'sex': 'Sexe',
            'phone': 'Téléphone',
            'nationality': 'Nationalité',
            'context': 'Contexte',
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_document': "Pièce d'identité",
            'id_number': "N° de la pièce d'identité",
            'status': 'Status de la visite',
        }
        widgets = {
            'host': forms.Select(attrs={'id': 'host_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sex': forms.Select(attrs={'id': 'sex_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'context': forms.Select(attrs={'id': 'context_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'arrived_at': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'departed_at': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_document': forms.Select(attrs={'id': 'id_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_number': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'status': forms.Select(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'observations': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:ring-1 focus:ring-purple-400 w-full"}),

        }


class AppointmentCreateForm(forms.ModelForm):
    # phone = PhoneNumberField()
    class Meta:
        model = Appointment
        fields = ('host',
                  'first_name',
                  'last_name',
                  'email',
                  'sex',
                  'phone',
                  'date',
                  'time',
                  'is_vip',)

        labels = {
            'host': 'Hôte',
            'first_name': 'Prénoms',
            'last_name': 'Nom',
            'email': 'Adresse Mail',
            'sex': 'Sexe',
            'phone': 'Téléphone',
            'date': "Date",
            'time': "Heure",
            'is_vip': 'Rendez-vous V.I.P',
        }
        widgets = {
            'host': forms.Select(attrs={'id': 'host_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sex': forms.Select(attrs={'id': 'sex_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'is_vip': forms.CheckboxInput(),

        }


class AppointmentEditForm(forms.ModelForm):
    # phone = PhoneNumberField()
    class Meta:
        model = Appointment
        fields = '__all__'

        labels = {
            'host': 'Hôte',
            'first_name': 'Prénoms',
            'last_name': 'Nom',
            'email': 'Adresse Mail',
            'phone': 'Téléphone',
            'sex': 'Sexe',
            'nationality': 'Nationalité',
            'date': "Date",
            'time': "Heure",
            'arrived_at': "Heure d'arrivée",
            'departed_at': 'Heure de départ',
            'id_document': "Pièce d'identité",
            'id_number': "N° de la pièce d'identité",
            'status': 'Status de la visite',
            'is_vip': 'Rendez-vous V.I.P',
        }
        exclude = ('started_at', 'ended_at', 'departed_at')
        widgets = {
            'host': forms.Select(attrs={'id': 'host_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sex': forms.Select(attrs={'id': 'sex_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'date': DateInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'arrived_at': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'departed_at': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_document': forms.Select(attrs={'id': 'id_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'id_number': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'status': forms.Select(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'is_vip': forms.CheckboxInput(),
            'observations': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:ring-1 focus:ring-purple-400 w-full"}),

        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ('manager', 'is_verified', 'employees', 'timestamp')

        labels = {
            'manager': 'Gestionaire',
            'name': 'Raison sociale',
            'slogan': 'Slogan',
            'company_type': "Type d'entreprise",
            'phone': 'Téléphone',
            'email': 'Adresse Mail',
            'description': 'Description',
            'workdays': 'Jours de travail',
            'opening_time': "Heure d'ouverture",
            'closing_time': "Heure de fermeture",
        }
        widgets = {

            'manager': forms.Select(attrs={'id': 'host_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'slogan': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'company_type': forms.Select(attrs={'id': 'comp_selector', 'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:ring-1 focus:ring-purple-400 w-full"}),
            'workdays': forms.CheckboxSelectMultiple(attrs={'class': ""}),
            'opening_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'closing_time': TimeInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }
