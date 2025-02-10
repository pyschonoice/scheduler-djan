from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task.settings')

app = Celery('task')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
     'check-probation-every-second': {
        'task': 'schedule_app.tasks.check_probation_periods',
        'schedule': 1.0,  # Run every 1 second.
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
