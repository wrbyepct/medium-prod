import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("medium_api")

app.config_from_object("core.celery.celeryconfig")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
    broker_transport_options={"visibility_timeout": 3600},
    task_soft_time_limit=300,  # 5 minute soft timeout
    task_time_limit=600,  # 10 minute hard timeout
)
