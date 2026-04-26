# config/settings/development.py
from .base import *


DEBUG = True


# SQLite for development — zero config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   BASE_DIR / 'db.sqlite3',
    }
}


# CORS — allow React dev server
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',   # Vite default port
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True


# Email — print to console in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


