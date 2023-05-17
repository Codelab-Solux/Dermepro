from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ''
        self.fields["email"].help_text = ''
        self.fields["first_name"].help_text = ''
        self.fields["last_name"].help_text = ''
        self.fields["password1"].help_text = ''
        self.fields["password2"].help_text = ''

        self.fields["username"].label = 'Pseudonyme'
        self.fields["email"].label = 'Adresse mail'
        self.fields["last_name"].label = 'Nom'
        self.fields["first_name"].label = 'Prenoms'
        self.fields["password1"].label = 'Mot de passe'
        self.fields["password2"].label = 'Confirmer le mot de passe'

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'password1': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'password2': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ''
        self.fields["email"].help_text = ''
        self.fields["first_name"].help_text = ''
        self.fields["last_name"].help_text = ''
        self.fields["password1"].help_text = ''
        self.fields["password2"].help_text = ''
        self.fields["tel"].help_text = ''
        self.fields["address"].help_text = ''
        self.fields["role"].help_text = ''

        self.fields["username"].label = 'Pseudonyme'
        self.fields["email"].label = 'Adresse mail'
        self.fields["last_name"].label = 'Nom'
        self.fields["first_name"].label = 'Prenoms'
        self.fields["password1"].label = 'Mot de passe'
        self.fields["password2"].label = 'Confirmer le mot de passe'
        self.fields["tel"].label = 'Telephone'
        self.fields["address"].label = 'Adresse'
        self.fields["role"].label = 'Role'

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'tel', 'address'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'password1': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'password2': forms.PasswordInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'role': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('__all__')
        exclude = ('role', 'groups', 'user_permissions',
                   'password', 'last_login', 'is_staff', 'is_superuser', 'is_active')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('__all__')
        exclude = ('groups', 'user_permissions', 'password',
                   'last_login', 'is_staff', 'is_superuser', 'is_active')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'tel': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'role': forms.Select(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }


class UserRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].label = 'Nom du role en Anglais'
        self.fields["fr_name"].label = 'Nom du role en Français'
        self.fields["sec_level"].label = 'Niveau de sécurité'

    class Meta:
        model = UserRole
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'fr_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
            'sec_level': forms.NumberInput(attrs={'class': "mb-2 px-4 py-2 rounded-md bg-white w-full"}),
        }
