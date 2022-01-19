from django.core.cache import cache


def get_item_from_cache(item_key):
    return cache.get(item_key)


def set_item_in_cache(item_key, item, time_out=None):
    cache.set(item_key, item)
