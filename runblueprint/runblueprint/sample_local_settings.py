from runblueprint.settings import *

# DO NOT USE THESE SETTINGS IN TEST, OR PROD

# Copy this file to your own local_settings.py file

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database name>',
        'USER': '<username>',
        'PASSWORD': '<some password>',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

from django.core.management.utils import get_random_secret_key
SECRET_KEY = get_random_secret_key()
