import os
from pathlib import Path

import dj_database_url
from environ import Env

from icecream import ic
from celery.schedules import crontab

env = Env()
Env.read_env()

ic.disable()

ENVIRONMENT = env("ENVIRONMENT", default="production")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

if ENVIRONMENT == "development":
    DEBUG = True
elif ENVIRONMENT == "production":
    DEBUG = False

ALLOWED_HOSTS = ["*"]

DEBUG = True
# Application definition

INSTALLED_APPS = [
    # Admin Panel Styling
    "unfold",
    
    # Default apps:
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # My apps:
    "dues",
    "account",
    "payments",
    
    # Third party apps:
    "admin_honeypot",
    "cloudinary_storage",
    "cloudinary",
    'django_celery_beat',
    'django_celery_results',
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
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

POSTGRES_LOCALLY = True

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ic("Database:", DATABASES)


if ENVIRONMENT == "production" or POSTGRES_LOCALLY is True:
    DATABASES["default"] = dj_database_url.parse(env("DATABASE_URL"))

ic('DATABASES["default"]: ', DATABASES["default"])

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"

if ENVIRONMENT == "production" or POSTGRES_LOCALLY is True:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env("CLOUD_NAME"),
    "API_KEY": env("CLOUD_API_KEY"),
    "API_SECRET": env("CLOUD_API_SECRET"),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.CustomUser"

LOGIN_REDIRECT_URL = "/index"
LOGIN_URL = "/account/login/"

PAYSTACK_PUBLIC_KEY = env("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = env("PAYSTACK_SECRET_KEY")

DEYWURO_USERNAME = env("DEYWURO_USERNAME")
DEYWURO_PASSWORD = env("DEYWURO_PASSWORD")
DEYWURO_SOURCE = env("DEYWURO_SOURCE")

ACCOUNT_USERNAME_BLACKLIST = [
    "admin",
    "accounts",
    "profile",
    "payments",
    "webmaster",
    "dues",
]

if ENVIRONMENT == 'production' or POSTGRES_LOCALLY is True:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = env("EMAIL_PORT", default=465)
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)
    EMAIL_USE_SSL = env("EMAIL_USE_SSL", default=True)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = f"MadrasatuPay {EMAIL_HOST_USER}"
    ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'send-monthly-reminders': {
        'task': 'payments.tasks.send_monthly_reminders',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
    'send-unpaid-dues-reminders': {
        'task': 'payments.tasks.send_unpaid_dues_reminders',
        'schedule': crontab(hour=0, minute=0),
    },
}
