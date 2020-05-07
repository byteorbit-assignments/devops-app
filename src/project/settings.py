"""
Project settings.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os

import environ
from django.utils.log import DEFAULT_LOGGING
from pkg_resources import get_distribution

env = environ.Env()

BASE_DIR = env('BASE_DIR', default='.')
BASE_URL = env('BASE_URL', default='http://localhost:8000')

PROJ_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(PROJ_DIR)

DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
SECRET_KEY = env('SECRET_KEY', default='(9#nNBZ=O$Tb3nFz(KknRyLfQ4Q7B-kAT=^*x)a2s$xM0%rK14')
SERVER_ENV = env('SERVER_ENV', default='dev')
VERSION = env('VERSION', default=get_distribution('devops-app').version)

INSTALLED_APPS = [
    'project',  # Project pkg has static,templates dirs. Keep at top.
    'apps.contact',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',

    # Add project apps here:
    # 'apps.users',
]

ROOT_URLCONF = 'project.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Staticfiles / Pipeline
# -----------------------------------------------------------------------------
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = env('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static_root'))
MEDIA_ROOT = env('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media_root'))
NPM_ROOT = env('NPM_ROOT', default=os.path.join(BASE_DIR, 'node_modules'))

CRISPY_TEMPLATE_PACK = 'bootstrap4'

if env('WHITENOISE', default=False):
    # WhiteNoise middleware should go after SecurityMiddleware
    _idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
    MIDDLEWARE.insert(_idx, 'whitenoise.middleware.WhiteNoiseMiddleware')
    WHITENOISE_AUTOREFRESH = DEBUG


# -----------------------------------------------------------------------------
DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR', default=False)
if DEBUG_TOOLBAR:
    INTERNAL_IPS = ['127.0.0.1']
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


# -----------------------------------------------------------------------------
DB_NAME = env('DB_NAME', default='devops-app')  # Also use as key prefix for cache
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'HOST': env('DB_HOST', default=''),
        'PORT': env('DB_PORT', default='5432'),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'ATOMIC_REQUESTS': True,
    }
}

REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/')
REDIS_CACHE_URL = env('REDIS_CACHE_URL', default=REDIS_URL + '0')
REDIS_QUEUE_URL = env('REDIS_QUEUE_URL', default=REDIS_URL + '1')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_URL,
        'KEY_PREFIX': DB_NAME,
        'VERSION': VERSION,
    },
}

# Use console mail backend by default -- will print mail to stdout instead of sending.
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Determine correct host, scheme when running behind a load balancer
if 'LOAD_BALANCER' in os.environ:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# -----------------------------------------------------------------------------
LOGGING = DEFAULT_LOGGING
LOGLEVEL = env('LOG', default='INFO')
LOGGING['loggers'].update({
    'apps': {
        'level': LOGLEVEL,
        'propagate': False,
        'handlers': ['django.server'],
    },
    # 'apps.pkg.module': ...,
})
# Silence dev server access logs (useful for pdb)
LOGGING['loggers']['django.server']['level'] = 'ERROR'
