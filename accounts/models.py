from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

# role_types = (
#     ('Administrateur', "Administrateur"),
#     ('Agent de sécurité', "Agent de sécurité"),
#     ('Directeur', "Directeur"),
#     ('Sécrétaire', "Sécrétaire"),
#     ('Utilisateur Général', "Utilisateur Général"),
# )


class Role(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    description = models.TextField(default='', null=True, blank=True)
    sec_level = models.IntegerField(default='0')

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be prvided')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pass
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, blank=True, null=True,)
    image = models.ImageField(blank=True, null=True, upload_to='users')

    # role = models.CharField(max_length=50, blank=True,
    #                         null=True, choices=role_types, default='general')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return f' {self.email.split("@")[0]}'
