from django.conf import settings

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nfqa',
            'HOST': 'localhost',
            'PORT': 3306,
            'USER': 'django-user',
            'PASSWORD': '123456',
        },
    'neo4j':
        {
            'HOST': "http://43.138.43.128:7474",
            "USER": "neo4j",
            "PASSWORD": 'neo4j',
        },
    'redis':
        {
            'HOST': "43.138.43.128",
            'PORT': 6379,
            "PASSWORD": "010209"
        }
}

REDIS_LOCATION = "redis://43.138.43.128:6379"
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
