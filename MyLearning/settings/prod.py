from .base import *

DEBUG = False

ADMINS = ('Zee', 'zubair1714@gmail.com')
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'edX',
    }
}
