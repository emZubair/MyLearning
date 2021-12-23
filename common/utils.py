from redis import Redis

from django.conf import settings


def get_redis_connector():
    redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    return redis
