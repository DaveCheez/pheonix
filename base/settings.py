import os
from pathlib import Path
from base.env import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="sagfhbfbshkcsfcafhghsfayetfdasdsyfjxhfhasfyegyegyd")

DEBUG = False;
#DEBUG = config("DEBUG_SETTING")
#DEBUG = os.getenv('DEBUG_SETTING', 'False').lower() == 'true'
#print("Debug: " , type(DEBUG), DEBUG)

#print("DJS: ", SECRET_KEY)
ALLOWED_HOSTS = ['phoenixvanz.com','https://coral-app-4w4xo.ondigitalocean.app/', '127.0.0.1', 'localhost', 'dev-phoenixvanz-wmmo3.ondigitalocean.app', 'dev.phoenixvanz.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nested_admin',
    'rest_framework',
    'accounts',
    'cart',
    'storages',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

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
                'store.views.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

from .db import *

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

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
else:
    from cdn.conf import *  # noqa
    STATIC_ROOT = STATIC_ROOT = BASE_DIR / "staticfiles-cdn" # dev example

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'staticfiles'),
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "https://dev-phoenixvanz-wmmo3.ondigitalocean.app", 
]

SESSION_COOKIE_SAMESITE = "Lax"  # or 'None' if cross-domain + HTTPS
SESSION_COOKIE_SECURE = True 