# have to be in gitignore, but i pushed it for review
import os


SHELL_PLUS = "ipython"

SITE_URL = '127.0.0.1:8000'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'qwer@mail.com'
EMAIL_HOST_PASSWORD = 'qwer1234'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SECRET_KEY = 'nce-vk6wu#8_(w%u9tcyx!*xem$un8rqf54rf1(xmarno*2g+$'

DEBUG = True

# I have used sqlite in test develop, so I duplicate BASE_DIR this
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
