import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('myshop')
# load every celery related settings from main settings.py with CELERY_prefix
app.config_from_object('django.conf:settings', namespace='CELERY')
# auto-discover asynchronous tasks for your applications. Celery will look
# for a tasks.py file in each application directory of applications added to
# INSTALLED_APPS in order to load asynchronous tasks defined in it.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
