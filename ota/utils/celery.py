from celery import Celery
from django.conf import settings


app = Celery(
    broker=f'redis://{settings.REDIS_URL}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
)