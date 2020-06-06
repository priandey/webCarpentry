from . import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webcarpentry',
        'USER': 'webcarpenter',
        'PASSWORD': 'pitour',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = '&nj!6wn2j-gjo90z^hsa#so866f)d+a0piu!&ovaltgnwwo#nw'

ALLOWED_HOSTS = []
