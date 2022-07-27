from .base import *
DEBUG = False
ADMINS = (
    ('Antonio M', 'mwarioxin@gmail.com.com'), # Errors will be sent to this emails
)
ALLOWED_HOSTS = ['*']
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'django_educa_prod',
       'USER': 'postgres',
       'PASSWORD': 'postgres',
   }
}