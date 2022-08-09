from django.conf import settings

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'NFQA',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'USER': 'root',
            'PASSWORD': '010209',
        },
    'neo4j':
        {
            'HOST': "http://localhost:7474",
            "USER": "neo4j",
            "PASSWORD": '010209',
        },
    'redis':
        {
            'HOST': "127.0.0.1",
            'PORT': 6379,
            "PASSWORD": "010209"
        }
}

REDIS_LOCATION = "redis://127.0.0.1:6379"
REDIS_AUTH = "010209"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_AUTH,
            "IGNORE_EXCEPTIONS": not settings.ENABLE_REDIS,
        }
    }
}
