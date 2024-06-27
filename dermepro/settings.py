"""
Django settings for dermepro project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from django.contrib import messages
from pathlib import Path
import dj_database_url
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=zwobp%lk7av6v7qoxcy%ungxo(2mg16@i()-r4ditye17kv3b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000/',
    "https://dermepro.onrender.com",
    # Add any other allowed origins as needed
]

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/',
                        'https://dermepro.onrender.com']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'django_htmx',
    'base',
    'accounts',
    'chats',
    'dj_database_url',
]

HASHIDS_SALT = 'SOLASCRIPTORA'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # custom middleware--------------------------------------
    'dermepro.middleware.HtmxMessageMiddleware',
]

ROOT_URLCONF = 'dermepro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


MESSAGE_TAGS = {
    messages.DEBUG: "w-full bg-gray-100 border rounded-lg px-4 py-2",
    messages.INFO: "w-full bg-blue-100 border border-blue-400  hover:bg-blue-200rounded-lg px-4 py-2",
    messages.SUCCESS: "w-full bg-green-100 border border-green-400 hover:bg-green-200 rounded-lg px-4 py-2",
    messages.WARNING: "w-full bg-amber-100 border border-amber-400 hover:bg-amber-200 rounded-lg px-4 py-2",
    messages.ERROR: "w-full bg-red-100 border border-g-red-400 hover:bg-red-200 rounded-lg px-4 py-2",
}

ASGI_APPLICATION = 'dermepro.asgi.application'
WSGI_APPLICATION = 'dermepro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': dj_database_url.parse('postgres://Codelab-Solux:CZRuAaG50cYp@ep-summer-surf-475106.us-east-2.aws.neon.tech/neondb')
    'default': {

        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'dermepro',
        # 'USER': 'postgres',
        # 'PASSWORD': 'password',
        # 'HOST': 'localhost',
        # 'PORT': '5432',

        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# NGINX setup--------------------------------------------------------------

# STATIC_URL = '/static/'
# STATIC_ROOT = '/app/static/'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = '/app/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field



# redis channel layer for render webservice
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('red-co09c4v79t8c73d97h90.redis.cache.windows.net', 6379)],
#         },
#     },
# }


# redis channel layer // MAKE SURE YOU GET REDIS RUNNING IN YOUR WSL BEFORE STARTING THE SERVER
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],  # Adjust host and port as needed
        },
    },
    
}

# windows in-memory channel layer
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# very important for the overiding of the default user model!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
AUTH_USER_MODEL = "accounts.CustomUser"  # new