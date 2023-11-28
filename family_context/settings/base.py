"""
Django settings for family_context project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys
from pathlib import Path

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")], default=""
)

CSRF_TRUSTED_ORIGINS = config(
    "TRUSTED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="https://127.0.0.1",
)

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOG_DESTINATION = config("LOG_DESTINATION", default="console")

# By default, log to console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "core": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(levelname)s] - %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
}

# add other logging output options.
if LOG_DESTINATION == "file":
    LOGGING["handlers"]["file"] = {
        "level": LOG_LEVEL,
        "class": "logging.FileHandler",
        "filename": "user_activity.log",
        "formatter": "verbose",
    }
    LOGGING["loggers"]["core"]["handlers"].append("file")


# Check if setting is set to allow this to run behind a load balancer
LOAD_BALANCER_SSL = config("LOAD_BALANCER_SSL", default=False, cast=bool)
if LOAD_BALANCER_SSL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "webpack_boilerplate",
    "django.contrib.postgres",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "core.middleware.PageViewLoggerMiddleware",
]

ROOT_URLCONF = "family_context.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "family_context", "templates"),
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATE_FORMAT = "%d %M %Y"
SHORT_DATE_FORMAT = "%d %m %Y"
DATE_INPUT_FORMATS = ["%d-%m-%Y"]

WSGI_APPLICATION = "family_context.wsgi.application"

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False

DEBUG_PROPAGATE_EXCEPTIONS = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend", "build"),
    os.path.join(BASE_DIR, "family_context", "static"),
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

WEBPACK_LOADER = {
    "MANIFEST_FILE": BASE_DIR / "frontend/build/manifest.json",
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
