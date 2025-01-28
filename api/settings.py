"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# for environment variable using django-environ library
# this allows you to use the .env file to set the environment variables
# throughout the entire application
# examle -
# from api.settings import env
# env("SECRET_VAR") # returns the value of the SECRET_VAR variable in the .env file
env = environ.Env(
    # Set casting and default values
    DEBUG=(bool, False),
    SECRET_KEY=(str, ""),
    ALLOWED_HOSTS=(list, []),
    DB_NAME=(str, ""),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, ""),
    DB_PORT=(str, ""),
    DB_URL=(str, ""),
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# False if not in os.environ because of casting above
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# Raises Django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    # "https://URL.com",
    # "https://www.URL.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    # "https://URL.com",
    # "https://www.URL.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


# Application definition

INSTALLED_APPS = [
    #####
    # Django Unfold admin panel
    #####
    "unfold",  # django-unfold
    "unfold.contrib.filters",  # django-unfold-filters
    "unfold.contrib.forms",  # django-unfold-forms
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    #####
    # Django core packages. Generated by django-admin startproject.
    #####
    "django.contrib.admin",  # admin
    "django.contrib.auth",  # auth
    "django.contrib.contenttypes",  # content types
    "django.contrib.sessions",  # sessions
    "django.contrib.messages",  # messages
    "django.contrib.staticfiles",  # static files
    #####
    # django-ninja-extra libraries
    #####
    "ninja_extra",  # django-ninja-extra
    "ninja_jwt",  # django-ninja-jwt
    #####
    # user created apps
    #####
    "core",  # core app
    "todos",  # todos app
    #####
    # third party packages
    #####
    "corsheaders",  # django-cors-headers for cross-origin requests
    "debug_toolbar",  # django-debug-toolbar for debugging
    "import_export",  # django-import-export for importing and exporting data
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # security middleware
    "django.contrib.sessions.middleware.SessionMiddleware",  # session middleware
    "corsheaders.middleware.CorsMiddleware",  # django-cors-headers
    "django.middleware.common.CommonMiddleware",  # common middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # csrf view middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # authentication middleware
    "django.contrib.messages.middleware.MessageMiddleware",  # message middleware
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  #  django-debug-toolbar
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # django templates
        "DIRS": [],  # directories
        "APP_DIRS": True,  # app directories
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # debug context processor
                "django.template.context_processors.request",  # request context processor
                "django.contrib.auth.context_processors.auth",  # auth context processor
                "django.contrib.messages.context_processors.messages",  # messages context processor
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"  # wsgi application

#####
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
#####

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # postgresql database
        "NAME": env("DB_NAME"),  # database name
        "USER": env("DB_USER"),  # database user
        "PASSWORD": env("DB_PASSWORD"),  # database password
        "HOST": env("DB_HOST"),  # database host
        "PORT": env("DB_PORT"),  # database port
    }
}


#####
# logging settings
#####
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "import_export": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "core": {  # Add logger for core app
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "core.schemas": {  # Add specific logger for schemas
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "core.controllers": {  # Add specific logger for controllers
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# This variable allows this get_user_model() throughout the app to be the User model located in core/models.py
AUTH_USER_MODEL = "core.User"
# example -
# from django.contrib.auth import get_user_model
# User = get_user_model()


#####
# Django Ninja JWT settings
#####

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),  # 5 minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 1 day
    "ROTATE_REFRESH_TOKENS": False,  # rotate refresh tokens
    "BLACKLIST_AFTER_ROTATION": False,  # blacklist after rotation
    "UPDATE_LAST_LOGIN": False,  # update last login
    "ALGORITHM": "HS256",  # algorithm
    "SIGNING_KEY": SECRET_KEY,  # signing key
    "VERIFYING_KEY": None,  # verifying key
    "AUDIENCE": None,  # audience
    "ISSUER": None,  # issuer
    "JWK_URL": None,  # jwk url
    "LEEWAY": 0,  # leeway
    "USER_ID_FIELD": "id",  # user id field
    "USER_ID_CLAIM": "user_id",  # user id claim
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",  # token user class
    "JTI_CLAIM": "jti",  # jti claim
    # For Controller Schemas
    # FOR OBTAIN PAIR
    "TOKEN_OBTAIN_PAIR_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainPairInputSchema",  # token obtain pair input schema
    "TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshInputSchema",  # token obtain pair refresh input schema
}


# https://eadwincode.github.io/django-ninja-extra/settings/
# Included pagination, throttling, ordering, and searching
NINJA_EXTRA = {
    "PAGINATION_CLASS": "ninja_extra.pagination.PageNumberPaginationExtra",  # included pagination
    "PAGINATION_PER_PAGE": 50,  # 50 items per page
    "INJECTOR_MODULES": [],  # injector modules
    "THROTTLE_CLASSES": [
        "ninja_extra.throttling.AnonRateThrottle",  # anonymous user throttling
        "ninja_extra.throttling.UserRateThrottle",  # authenticated user throttling
    ],
    "THROTTLE_RATES": {
        "user": "1000/day",  # 1000 requests per day for authenticated users
        "anon": "100/day",  # 100 requests per day for anonymous users
    },
    "NUM_PROXIES": None,  # number of proxies
    "ORDERING_CLASS": "ninja_extra.ordering.Ordering",  # included ordering
    "SEARCHING_CLASS": "ninja_extra.searching.Search",  # included searching
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"  # language code
TIME_ZONE = "UTC"  # time zone
USE_I18N = True  # use i18n
USE_TZ = True  # use tz


#####
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
#####

STATIC_URL = "static/"
STATIC_ROOT = "static/"

# Media files
# MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#####
# django-debug-toolbar
#####

INTERNAL_IPS = [
    "127.0.0.1",  # localhost
]
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",  # history panel
    "debug_toolbar.panels.versions.VersionsPanel",  # versions panel
    "debug_toolbar.panels.timer.TimerPanel",  # timer panel
    "debug_toolbar.panels.settings.SettingsPanel",  # settings panel
    "debug_toolbar.panels.headers.HeadersPanel",  # headers panel
    "debug_toolbar.panels.request.RequestPanel",  # request panel
    "debug_toolbar.panels.sql.SQLPanel",  # sql panel
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",  # static files panel
    "debug_toolbar.panels.templates.TemplatesPanel",  # templates panel
    "debug_toolbar.panels.alerts.AlertsPanel",  # alerts panel
    "debug_toolbar.panels.cache.CachePanel",  # cache panel
    "debug_toolbar.panels.signals.SignalsPanel",  # signals panel
    "debug_toolbar.panels.redirects.RedirectsPanel",  # redirects panel
    "debug_toolbar.panels.profiling.ProfilingPanel",  # profiling panel
]
