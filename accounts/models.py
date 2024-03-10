from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from base.utils import h_encode, h_decode



class Role(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    description = models.TextField(default='', null=True, blank=True)
    sec_level = models.IntegerField(default='0')

    def get_hashid(self):
        return h_encode(self.id)

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
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, blank=True, null=True,)
    image = models.ImageField(blank=True, null=True, upload_to='users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return f' {self.email.split("@")[0]}'



class UserStatus(models.Model):
    title = models.CharField(max_length = 255)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('status', kwargs={'pk': self.pk})


gender_list = (
    ('female', 'Féminin'),
    ('male', 'Masculin'),
)

# from base.models import Company
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey('base.Company', on_delete=models.CASCADE, blank=True, null=True)
    reg_number = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=1000, null=True, blank=True)
    sex = models.CharField(
        max_length=10, choices=gender_list, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    status_message = models.CharField(max_length=200, default='Je suis disponible.', null=True, blank=True)
    status = models.ForeignKey(UserStatus, default=1, on_delete=models.CASCADE)
    phone_alt = PhoneNumberField(unique=True, blank=True, null=True)
    image = models.ImageField(
        upload_to='media/users/profiles', default='../static/imgs/anon.png', blank=True, null=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} - Profile'

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
