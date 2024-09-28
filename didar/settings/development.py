from .base import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# debug-toolbar middleware as early as possible in the list
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE