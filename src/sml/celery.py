from django.conf import settings

from celery import Celery

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sml.settings')

app = Celery('sml')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'send-auction-finished-email': {
        'task': 'sml_auction.tasks.send_auction_finished_email',
        'schedule': 300.0,
    },
}
app.conf.broker_url = settings.BROKER_URL

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
