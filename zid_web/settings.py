import boto3
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Loads environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))
ENVIRONMENT = os.getenv('ENVIRONMENT')
SSM = boto3.client('ssm')

os.environ['API_KEY'] = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/vatusa/api-key',
    WithDecryption=True
)['Parameter']['Value']
os.environ['ULS_K_VALUE'] = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/vatusa/k-value',
    WithDecryption=True
)['Parameter']['Value']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/django/secret-key',
    WithDecryption=True
)['Parameter']['Value']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('ENVIRONMENT').lower() != 'prod'

ALLOWED_HOSTS = [
    '.amazonaws.com',
    'zidartcc.org',
    'localhost',
    '.zidbase-dev.name',
    '.zidbase-dev.alpha'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.administration',
    'apps.api.apps.ApiConfig',
    'apps.event',
    'apps.feedback',
    'apps.pilots',
    'apps.resources',
    'apps.uls',
    'apps.user.apps.UserConfig',
    'apps.views'
]

MIDDLEWARE = [
    # TODO: This module cannot be used until it supports Django 2.0
    # Pull requests exist to fix the issue but no apparent progress
    # 'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'zid_web.middleware.UserMiddleware',
]

ROOT_URLCONF = 'zid_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
            'libraries': {
                'extras': 'apps.views.templatetags.extras'
            }
        },
    },
]

WSGI_APPLICATION = 'zid_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SSM.get_parameter(
            Name=f'/zid/{ENVIRONMENT}/db/database'
        )['Parameter']['Value'],
        'USER': SSM.get_parameter(
            Name=f'/zid/{ENVIRONMENT}/db/username'
        )['Parameter']['Value'],
        'PASSWORD': SSM.get_parameter(
            Name=f'/zid/{ENVIRONMENT}/db/password',
            WithDecryption=True
        )['Parameter']['Value'],
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

EMAIL_HOST = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/smtp/host'
)['Parameter']['Value']
EMAIL_PORT = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/smtp/port'
)['Parameter']['Value']
EMAIL_HOST_USER = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/smtp/username'
)['Parameter']['Value']
EMAIL_HOST_PASSWORD = SSM.get_parameter(
    Name=f'/zid/{ENVIRONMENT}/smtp/password'
)['Parameter']['Value']
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS').lower() == 'true'
DEFAULT_FROM_EMAIL = 'Do Not Reply <no-reply@zidartcc.org>'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
