"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u@#qfdzhhp$e8xgihk$sp!u&-_=8gwxc&ainq&j0ec&0azs6@d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', # this app gives us an interface managing the data
    'django.contrib.auth', # this app is used for authenticating the users
    'django.contrib.contenttypes',
    # the session is legency, we don't use it anymore.
    'django.contrib.sessions',
    'django.contrib.messages',# used for displaying one time notifications fo the user
    'django.contrib.staticfiles',# for serving static files
    # restful framework should be here
    'rest_framework',
    'djoser',
    'django_filters',

    # my apps
    'playground',
    'debug_toolbar',  # for django-debug-toolbar
    'store',

    'tags',
    'likes',
    'core',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # inspect the incomming request and if there is information about user,
    # it will retrieve that user from the database and attach it to the request object
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from . import secrets
SSL_DIR = BASE_DIR / 'project' / 'mysql_ssl'
ca_path = SSL_DIR / 'ca.pem'
cert_path = SSL_DIR / 'client-cert.pem'
key_path = SSL_DIR / 'client-key.pem'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets.DATABASE_NAME,
        'USER': secrets.DATABASE_USER,
        'PASSWORD': secrets.DATABASE_PASSWORD,
        'HOST': secrets.DATABASE_HOST,   # Set to empty string for localhost.
        'PORT': secrets.DATABASE_PORT,            # Set to empty string for default.

        'OPTIONS': {
            'ssl': {
                'ca': str(ca_path),
                'cert': str(cert_path),
                'key': str(key_path),
            }
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# the prerequisites of the password
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
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FtoFiIELD = 'django.db.models.BigAueld'


# 比如"unit_price" 的值是decimal， 但是 传回来见的 json 是 string 格式，这里设置一下
REST_FRAMEWORK= {
    "COERCE_DECIMAL_TO_STRING": False,
    # "PAGE_SIZE": 5,
    # enable pagenation for all models
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination"

    # https://djoser.readthedocs.io/en/latest/authentication_backends.html#json-web-token-authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),


}


# define a self-defined User(but we defined this too late, we should define it before starting the Project)
AUTH_USER_MODEL = "core.User"

# for handling the customized serilizers in DJOSER
DJOSER = {
    "SERIALIZERS": {
        "user_create": "core.serializers.UserCreateSerializer",
        "current_user": "core.serializers.UserSerializer"
    }
}

# for authentication, change the token time(不想那么快 login 失效)
# Ein JWT besteht typischerweise aus drei Teilen, die durch Punkte voneinander getrennt sind: Header,
# Payload und Signature. Also sieht ein JWT so aus: xxxxx.yyyyy.zzzzz.
# Header: Der Header enthält typischerweise zwei Teile: den Typ des Tokens, der JWT ist,
# und den verwendeten Hashing-Algorithmus, wie zum Beispiel HMAC SHA256 oder RSA.
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}