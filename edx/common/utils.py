from django.core.cache import cache


def get_item_from_cache(item_key):
    return cache.get(item_key)


def set_item_in_cache(item_key, item, time_out=None):
    cache.set(item_key, item)


def my_middleware(get_response):
    def middleware(request):
        # Code executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        # Code executed for each request/response after
        # the view is called.
        return response
    return middleware
