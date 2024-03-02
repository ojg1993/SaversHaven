import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'default_key')

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Application definition

INSTALLED_APPS = [
    'daphne',  # ASGI server for channel

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Internal_apps
    'core',
    'user',
    'address',
    'product',
    'chat',
    'transaction',
    'review',

    # External_apps
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'corsheaders',
    'channels',

    # Authentication
    'rest_framework.authtoken',  # drf token auth
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',  # local account related
    'allauth.socialaccount',  # social login support
    'allauth.socialaccount.providers.google'  # google login
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Cross Origin
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # "allauth.account.middleware.AccountMiddleware", # django-allauth
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/static/'
STATIC_ROOT = '/vol/web/static/'

MEDIA_URL = '/static/media/'
MEDIA_ROOT = '/vol/web/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

ACCOUNT_ADAPTER = 'user.adapters.CustomAccountAdapter'


# Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_MAIL = EMAIL_HOST_USER
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Saven]'


# drf config
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
}


# djangorestframework-simplejwt config
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ('Bearer'),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "SIGNING_KEY": SECRET_KEY,
}


# dj-rest-auth config
REST_AUTH_TOKEN_MODEL = None
REST_USE_JWT = True
REST_SESSION_LOGIN = False
JWT_AUTH_COOKIE = 'saven-auth'
JWT_AUTH_REFRESH_COOKIE = 'saven-auth-refresh'
JWT_AUTH_HTTPONLY = False
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "user.serializers.UserSerializer"
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "user.serializers.CustomRegisterSerializer",
}


# django-allauth config
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # none / mandatory
ACCOUNT_EMAIL_VERIFICATION_EXPIRATION = 1
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'


# drf-spectacular config
SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api',
    'COMPONENT_SPLIT_REQUEST': True,
}

SOCIAL_AUTH_GOOGLE_CLIENT_ID = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET')
STATE = 'qwewqeqwetgljhn4ilb23uy'


# channels config
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
    # 'default': {
    #     'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #     'CONFIG': {
    #         'hosts': [('127.0.0.1', os.environ.get('REDIS_PORT'))],
    #     },
    # },
}
