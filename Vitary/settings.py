import os
from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-od1y3j(!1bl7)s%n#1$xh1%p=v4q6-l$%&zns_18nv!mj_b_m!",
)

DEBUG = env("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.sitemaps",
    "apps.api.apps.ApiConfig",
    "apps.core.apps.CoreConfig",
    "apps.account.apps.AccountsConfig",
    "apps.feed.apps.VitConfig",
    "apps.blog.apps.BlogConfig",
    "apps.notification.apps.NotificationConfig",
    "apps.chat.apps.ChatConfig",
    "django_cleanup.apps.CleanupConfig",
    "bulma",
    "loginas",
    "corsheaders",
    "graphene_django",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Vitary.urls"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-api-key",
)

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
                "apps.core.context_processors.web_url",
                "apps.core.context_processors.random_color",
                "apps.core.context_processors.is_debug",
                "apps.core.context_processors.frontpage_data",
                "apps.core.context_processors.is_htmx",
                "apps.notification.context_processors.get_notification_info",
                "apps.feed.context_processors.get_latest_feeds",
                "apps.feed.context_processors.feed_form",
            ],
        },
    },
]


WSGI_APPLICATION = "Vitary.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    DEFAULT_FROM_EMAIL = env("EMAIL_ADDRESS")
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = env("EMAIL_ADDRESS")
    EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")


SITE_ID = int(env("SITE_ID", default=1))

WEB_HOST = env("WEB_HOST", default="http://localhost:8000")

SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default=False)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=False)


MANAGERS = [("foxy4096", "adityapriyadarshi669@gmail.com")]
ADMIN = [("foxy4096", "adityapriyadarshi669@gmail.com")]


GRAPHENE = {
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_ALLOW_ARGUMENT": True,
}
