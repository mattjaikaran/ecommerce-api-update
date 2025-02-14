from functools import wraps
from django.core.cache import cache
from .settings import cache_key_prefix, CACHE_TTL

def cached_view(timeout=CACHE_TTL, key_prefix='view'):
    """
    Cache decorator for API views.
    Usage:
        @cached_view(timeout=300, key_prefix='products')
        def get_products(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Generate cache key based on the full URL path and query parameters
            cache_key = f"{key_prefix}:{request.get_full_path()}"
            response = cache.get(cache_key_prefix(cache_key))
            
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key_prefix(cache_key), response, timeout)
            
            return response
        return _wrapped_view
    return decorator

def cached_method(timeout=CACHE_TTL, key_prefix='method'):
    """
    Cache decorator for class methods.
    Usage:
        @cached_method(timeout=300, key_prefix='user')
        def get_user_data(self, user_id):
            ...
    """
    def decorator(method):
        @wraps(method)
        def _wrapped_method(self, *args, **kwargs):
            # Generate cache key based on method arguments
            cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
            if kwargs:
                cache_key += f":{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"
            
            result = cache.get(cache_key_prefix(cache_key))
            
            if result is None:
                result = method(self, *args, **kwargs)
                cache.set(cache_key_prefix(cache_key), result, timeout)
            
            return result
        return _wrapped_method
    return decorator
