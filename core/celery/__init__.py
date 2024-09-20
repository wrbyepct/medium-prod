import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("medium_api")

app.config_from_object("core.celery.celeryconfig")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
