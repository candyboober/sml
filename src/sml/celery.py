import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sml.settings')

app = Celery('sml')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.BROKER_URL
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
