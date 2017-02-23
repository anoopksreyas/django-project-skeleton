from __future__ import absolute_import
 
import os
 
from celery import Celery
 
from django.conf import settings
 
# Indicate Celery to use the default Django settings module 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
 
app = Celery('{project_name}', broker='amqp://', backend='amqp://')
 
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
 
 
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))