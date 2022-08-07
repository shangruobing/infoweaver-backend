import os
import datetime
from pathlib import Path

# !!!通过设置是否开发模式，来动态修改数据库配置文件和是否Debug
is_development_mode = True
# is_development_mode = False

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-k+@gtqz^w72bt^-(mpd7d%j^_8b7@0wg7hq9!=l(y^+wwws=sh'

DEBUG = is_development_mode

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'QAS'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'NFQA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NFQA.wsgi.application'

if is_development_mode:
    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'NFQA',
                'HOST': '127.0.0.1',
                'PORT': 3306,
                'USER': 'root',  # 数据库用户名 需要更改！
                'PASSWORD': '010209',  # 数据库密码 需要更改！
            },
        'neo4j':
            {
                'HOST': "http://localhost:7474",
                "USER": "neo4j",  # 图数据库用户名 需要更改！
                "PASSWORD": '010209',  # 图数据库密码 需要更改！
            }
    }

else:
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
            }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UPLOAD_FILE_STORAGE = '/media/upload/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        'rest_framework.parsers.JSONParser'
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "QAS.authentication.JWTAuthentication"
    ],
    #     "DEFAULT_PERMISSION_CLASSES": [
    #         "rest_framework.permissions.IsAuthenticated",
    #     ],
    #
    "DEFAULT_THROTTLE_CLASSES": [
        "QAS.throttle.GenericThrottle"
    ],
    #
    #     "DEFAULT_THROTTLE_RATES": {
    #         "mySimpleThrottle": '10/m'
    #     },
    #
    "DEFAULT_PAGINATION_CLASS": {
        'QAS.pagination.GenericPagination'
    }
}

APPEND_SLASH = True

JWT_AUTH = {
    # token过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 允许刷新
    'JWT_ALLOW_REFRESH': True,
    # 刷新的过期时间
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_AUTH_HEADER_PREFIX': 'JWT'
}

AUTH_USER_MODEL = 'QAS.User'  # 自定义用户表

# REDIS_TIMEOUT=10
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379",
#         "OPTIONS": {
#             # 忽略连接异常
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "IGNORE_EXCEPTIONS": True,
#         }
#     }
# }
