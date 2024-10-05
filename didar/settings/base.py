"""
Django settings for Didar project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    # Local apps
    'users',
    'faculty',
    'schedule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # django white-noise
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # django-cors-headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'didar.urls'

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

WSGI_APPLICATION = 'didar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# rest-framework configs
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.api.custom_pagination.CustomLimitOffsetPagination',
    'PAGE_SIZE': 36,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/minute",
        "user": "90/minute",
    },

    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "ALLOWED_VERSIONS": ["v1"],
}

# simple jwt configs
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "SIGNING_KEY": SECRET_KEY,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,  # does not affect when blacklist app is not listed
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    # "VERIFYING_KEY": None, # Only for RSA algorithm
    "AUDIENCE": None,
    "ISSUER": "TICLIX",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": lambda user: user is not None
    and user.is_active,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=5),
}

# Schema configs
SPECTACULAR_SETTINGS = {
    "TITLE": "Didar",
    "DESCRIPTION": """Didar API documentation.\n\nNote that all success responses are in a `data` object.\n\n
    For example an empty success response is:
    {
        "success": true,
        "data": { }
    }
    Also all error responses is like below:
    {
        "success": false,
        "error": {
            "code": int,
            "msg": "string"
            }
    }
    """,
    "TOS": None,
    "CONTACT": {
        "name": "Didar Backend Team",
        "email": "m.asgari1589@gmail.com",
    },
    # "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
}

# Logging config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "console_debug": {
            "format": "{levelname} {name} {asctime} {pathname} {module} {funcName} {lineno} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {name} {asctime} {pathname} {module} {funcName} {lineno} {message}",
            "style": "{",
            # "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console_debug": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "console_debug",
        },
        "verbose": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "debug_logging": {
            "handlers": [
                "console_debug",
            ],
            "level": "DEBUG",
            "propagate": True,
        },
        # "" for all logs
        "stdout_logging": {
            "handlers": [
                "verbose",
            ],
            "level": "INFO",
            "propagate": True,
        },
    },
}

