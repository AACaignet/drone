from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks',broker = 'redis://redis:6379/0',include=['api.celery.tasks'] )

#app.config_from_object('celeryconfig')

#app.autodiscover_tasks(['tasks'])
app.conf.beat_schedule = {
    'check_battery': {
        'task': 'api.celery.tasks.check_battery',
        'schedule': timedelta(minutes=1),
        #'args': (16, 16)
    },
     'check_drone_state': {
        'task': 'api.celery.tasks.check_drone_state',
        'schedule': timedelta(minutes=2),
        #'args': (16, 16)
    }
}
app.conf.timezone   = 'Cuba'
app.conf.enable_utc   = True
