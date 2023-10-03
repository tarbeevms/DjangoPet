# Caching

CACHES = {
    'default': {
        # use some other cache in production,
        # like https://github.com/jazzband/django-redis
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
