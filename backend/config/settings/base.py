# config/settings/base.py
import environ
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')


SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]


LOCAL_APPS = [
    'core',
    'accounts',
    'customers',
    'products',
    'inventory',
    'orders',
    'production',
    'finance',
    'reports',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]


WSGI_APPLICATION = 'config.wsgi.application'


# Custom User Model
AUTH_USER_MODEL = 'accounts.User'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Argon2 password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]


# Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Africa/Accra'
USE_I18N      = True
USE_TZ        = True


# Static files
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Django REST Framework ──────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardResultsPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}


# ── SimpleJWT — Phase 1 (Single long-lived token) ─────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':    timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME':   timedelta(days=30),
    'ROTATE_REFRESH_TOKENS':    False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES':        ('Bearer',),
    'ALGORITHM':                'HS256',
    'USER_ID_FIELD':            'id',
    'USER_ID_CLAIM':            'user_id',
}


# ── Djoser ────────────────────────────────────────────────────
DJOSER = {
    'LOGIN_FIELD':                  'email',
    'USER_CREATE_PASSWORD_RETYPE':  True,
    'SEND_ACTIVATION_EMAIL':        False,
    'PASSWORD_RESET_CONFIRM_URL':   False,
    'TOKEN_MODEL':                  None,   # Use JWT, not DRF Token
    'SERIALIZERS': {
        'user':         'accounts.serializers.UserSerializer',
        'current_user': 'accounts.serializers.UserSerializer',
    },
}


# ── drf-spectacular (Swagger) ──────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE':       'NBN Enterprise API',
    'DESCRIPTION': 'Manufacturing & Sales Management System API',
    'VERSION':     '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


# ── Currency (system-wide constant) ───────────────────────────
CURRENCY = 'GHS'
CURRENCY_SYMBOL = '\u20b5'


