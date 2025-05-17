import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MonTool.settings")

app=Celery("celery_app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["celery_tasks"])

app.conf.beat_schedule = {
    "connection_quality": {"task": "celery_tasks.tasks.connection_quality",
                  "schedule": timedelta(minutes=1)},
}