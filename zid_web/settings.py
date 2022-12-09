import django_heroku
import os

from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Loads environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))
ENVIRONMENT = os.getenv('ENVIRONMENT')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT.lower() != 'prod'
CSRF_TRUSTED_ORIGINS = [f'https://{os.getenv("WEBSITE_DOMAIN")}',
                        f'https://*.{os.getenv("WEBSITE_DOMAIN")}']

ALLOWED_HOSTS = [
    f'{os.getenv("WEBSITE_DOMAIN")}',
    f'.{os.getenv("WEBSITE_DOMAIN")}'
]

if os.getenv('ALLOWED_CIDR', False):
    ALLOWED_CIDR_NETS = [os.getenv('ALLOWED_CIDR')]


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
    'apps.news',
    'apps.pilots',
    'apps.resources',
    'apps.sso',
    'apps.training',
    'apps.user.apps.UserConfig',
    'apps.views'
]

MIDDLEWARE = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'zid_web.middleware.UserMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware'
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'applog': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/app.log'),
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['applog', 'console'],
            'level': 'WARNING',
            'propagate': True
        },
        'apps': {
            'handlers': ['applog', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'util': {
            'handlers': ['applog', 'console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

WSGI_APPLICATION = 'zid_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Do Not Reply <noreply@zidartcc.org>'


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

django_heroku.settings(locals())
