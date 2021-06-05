import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electroshop.settings.dev')
# app = Celery(main='electroshop', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(main='electroshop', broker='amqp://ehsan:Ehsan1992@localhost:5672/ehsanhost', backend='amqp://ehsan:Ehsan1992@localhost:5672/ehsanhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
