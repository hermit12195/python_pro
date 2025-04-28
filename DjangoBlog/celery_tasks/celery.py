import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBlog.settings")

app=Celery("celery_app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["celery_tasks"])

app.conf.beat_schedule = {
    "user_quantity": {"task": "celery_tasks.tasks.user_quantity",
                  "schedule": timedelta(minutes=10)}
}
