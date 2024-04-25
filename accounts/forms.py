from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"
        self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"
        self.fields['password1'].label = "Mot de pass"
        self.fields['password2'].label = "Confirmez votre mot de pass"

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
        )
        labels = {'username': "Nom d'utilisateur", 'email': 'Email',
                  'first_name': 'Prenoms', 'last_name': 'Nom', 'phone': 'Telephone', }
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-gray-100 w-full"}),
            'role': forms.Select(attrs={'id': 'role_selector',  'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"
        self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"
        self.fields['password1'].label = "Mots de pass"
        self.fields['password2'].label = "Confirmez mots de pass"

    class Meta:
        model = CustomUser
        fields = (
            'role', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
            'phone',
            #  'address'
        )
        labels = {'username': "Nom d'utilisateur", 'email': 'Email',
                  'first_name': 'Prenoms', 'last_name': 'Nom',
                  'phone': 'Telephone',
                  #   'address': 'Adresse'
                  }
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'password1': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'password2': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'role': forms.Select(attrs={'id': 'role_selector',  'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('__all__')
        exclude = (
            'role', 'groups', 'user_permissions', 'password', 'last_login', 'is_staff', 'is_superuser', 'is_active')
        labels = {'username': "Nom d'utilisateur", 'email': 'Email', 'first_name': 'Prenoms', 'last_name': 'Nom', 'phone': 'Telephone', 'address': 'Adresse'
                  }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('__all__')
        # exclude = (
        #     'user', 'company', 'status', 'is_online', 'status_message')
        labels = {'reg_number': "Numero d'immatriculation", 'sex': 'Sexe', 'department': 'Departement',
                  'nationality': 'Nationalité', 'job_position': 'Poste', 'phone_alt': 'Telephone'
                  }
        widgets = {
            'reg_number': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'nationality': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sex': forms.Select(attrs={'id':"sex_selector", 'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'birthday': DateInput(attrs={'class': "mb-2 px-3 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'bio': forms.Textarea(attrs={'placeholder': 'Bio', "rows": "4", 'class': "mb-2 px-4 py-2 rounded-md border border-gray-200 focus:border-none focus:outline-none focus:ring-2 focus:ring-green-300 w-full"}),
            'department': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'job_position': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'status_message': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone_alt': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('__all__')
        exclude = ('groups', 'user_permissions', 'password',
                   'last_login', 'is_staff', 'is_superuser', 'is_active')
        labels = {'username': "Nom d'utilisateur", 'email': 'Email',
                  'first_name': 'Prenoms', 'last_name': 'Nom',
                  'phone': 'Telephone', 'address': 'Adresse'
                  }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'role': forms.Select(attrs={'id': 'role_selector',  'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class TimeManagementForm(forms.ModelForm):
    class Meta:
        model = TimeManagement
        fields = ('user','user_password',)
        labels = {'user': "Utilisateur", 
                  'user_password': 'Mots de passe',
                  }
        widgets = {
            'user': forms.Select(attrs={'id': 'role_selector',  'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'user_password': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].label = 'Nom du role'
        self.fields["description"].label = 'Description du role'
        self.fields["sec_level"].label = 'Niveau de sécurité'

    class Meta:
        model = Role
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'description': forms.Textarea(attrs={"rows": "10", 'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
            'sec_level': forms.NumberInput(attrs={'class': "mb-2 px-4 py-2 rounded-md border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-purple-400 w-full"}),
        }
