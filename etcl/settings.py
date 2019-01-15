"""
Django settings for etcl project.

Generated by 'django-admin startproject' using Django 1.8.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
SECRET_KEY = 'j8dwfg6kvg=fnfs33s0x(t&0pfe)p9$3dm943)6hvurj6@=+4j'
DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', 'localhost']
WSGI_APPLICATION = 'etcl.wsgi.application'


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'proposals',
    'studies',
    'tasks',
    'interventions',
    'observations',
    'reviews',
    'feedback',
    'faqs',

    'easy_pdf',
    'modeltranslation',

    'django.contrib.admin',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

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

ROOT_URLCONF = 'etcl.urls'

LOGIN_REDIRECT_URL = '/'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    #'mysql': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'ethics',
    #    'USER': 'root',
    #    'PASSWORD': 'root++',
    #}
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'nl-NL'
LANGUAGES = (
    ('nl', _('Nederlands')),
    ('en', _('Engels')),
)
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    'locale',
)

TIME_ZONE = 'Europe/Amsterdam'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# File handling
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

# E-mail settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525
EMAIL_FROM = 'T.D.Mees@uu.nl'
EMAIL_LOCAL_STAFF = 'T.D.Mees@uu.nl'


# Group names
GROUP_SECRETARY = 'Secretaris'
GROUP_COMMISSION = 'ETCL' # TODO: rename variable to ETCL
GROUP_FETC = 'FETC'

# Route durations
PREASSESSMENT_ROUTE_WEEKS = 1
SHORT_ROUTE_WEEKS = 2

# Base URL
BASE_URL = '127.0.0.1:8000'

try:
    from .ldap_settings import *
except ImportError:
    print('Proceeding without LDAP settings')
