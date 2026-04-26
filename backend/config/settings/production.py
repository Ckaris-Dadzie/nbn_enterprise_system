# config/settings/production.py
from .base import *


DEBUG = False


# PostgreSQL — reads from .env
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     env('DB_NAME'),
        'USER':     env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST':     env('DB_HOST', default='localhost'),
        'PORT':     env('DB_PORT', default='5432'),
    }
}


# CORS — restrict to production domain
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True


# Security
SECURE_SSL_REDIRECT         = True
SESSION_COOKIE_SECURE       = True
CSRF_COOKIE_SECURE          = True
SECURE_BROWSER_XSS_FILTER  = True
SECURE_CONTENT_TYPE_NOSNIFF = True
