import os

import django_heroku

from .base import *

ALLOWED_HOSTS = ['https://social-network-aholovlov.herokuapp.com/']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

django_heroku.settings(locals())
