from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from configurations import Configuration

from django.utils.functional import cached_property

from .values import from_environ


class Base(Configuration):  # type: ignore[misc]
    log = logging.getLogger(__name__)

    PROJECT_NAME = "B2Broker"
    PROJECT_BASE_URL = from_environ("http://localhost", name="B2B_PROJECT_BASE_URL")
    # Project environment (e.g., "stage", "prod", "production").
    PROJECT_ENVIRONMENT = from_environ("unknown")
    # Fix relative MEDIA_URL and STATIC_URL to absolute ones using PROJECT_BASE_URL
    FIX_RELATIVE_URLS = from_environ(True)

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    ALLOWED_HOSTS: list[str] = []
    CSRF_TRUSTED_ORIGINS: list[str] = []

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = from_environ("dummy")

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "django_extensions",
        "django_filters",
        "rest_framework",
        "rest_framework.authtoken",
        "drf_spectacular",

        "b2broker.billings.apps.BillingsConfig",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "b2broker.urls"
    WSGI_APPLICATION = "b2broker.wsgi.application"
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # Database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": from_environ(name="B2B_DB_NAME"),
            "USER": from_environ(name="B2B_DB_USER"),
            "PASSWORD": from_environ(name="B2B_DB_PASSWORD"),
            "HOST": from_environ(name="B2B_DB_HOST"),
            "PORT": from_environ(name="B2B_DB_PORT", type=int),
        },
    }

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    LANGUAGE_CODE = "en-US"
    TIME_ZONE = "Europe/Moscow"
    USE_I18N = True
    USE_TZ = True

    # STATIC
    STATIC_URL = from_environ("/staticfiles/", name="B2B_STATIC_URL")
    STATIC_ROOT = PROJECT_ROOT / "staticfiles"

    # MEDIA
    MEDIA_URL = from_environ("/media/", name="B2B_MEDIA_URL")
    MEDIA_ROOT = PROJECT_ROOT / "media"

    # TEMPLATES
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
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

    # AUTHENTICATION
    LOGIN_URL = "/"
    LOGIN_REDIRECT_URL = "/"
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
    ]

    # EMAIL
    DEFAULT_FROM_EMAIL = "notify@b2broker.ru"
    DEFAULT_SENDER = f"{PROJECT_NAME} <{DEFAULT_FROM_EMAIL}>"
    DEFAULT_TO_EMAIL: list[str] = []

    @cached_property
    def LOGGING(self) -> dict[str, Any]:  # noqa: N802
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "[ %(levelname)-7s ] %(asctime)s %(name)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }

    # REST_FRAMEWORK
    DEFAULT_SMALL_PAGE_SIZE: int = 10
    REST_FRAMEWORK = {
        "PAGE_SIZE": DEFAULT_SMALL_PAGE_SIZE,
        "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
        "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
        "DEFAULT_PARSER_CLASSES": [
            "rest_framework_json_api.parsers.JSONParser",
        ],
        "DEFAULT_RENDERER_CLASSES": ["rest_framework_json_api.renderers.JSONRenderer"],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "b2broker.api.authentication.TokenAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
        "DEFAULT_FILTER_BACKENDS": ["rest_framework_json_api.django_filters.DjangoFilterBackend"],
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "SEARCH_PARAM": "filter[search]",
        "TEST_REQUEST_RENDERER_CLASSES": [
            "rest_framework_json_api.renderers.JSONRenderer",
        ],
        "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular_jsonapi.schemas.openapi.JsonApiAutoSchema",
    }

    @cached_property
    def SPECTACULAR_SETTINGS(self) -> dict[str, Any]:  # noqa: N802
        return {
            "TITLE": f"{self.PROJECT_NAME} API",
            "VERSION": None,
            "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+/",
            "SCHEMA_PATH_PREFIX_TRIM": True,
            "SERVE_AUTHENTICATION": ["rest_framework.authentication.SessionAuthentication"],
            "SERVE_PERMISSIONS": ["b2broker.api.permissions.IsSuperUser"],
            "SERVERS": [{"url": f"{self.PROJECT_BASE_URL}/api/v1"}],
            # JSON API
            # provide different schema components for patch and post
            "COMPONENT_SPLIT_REQUEST": True,
            # fix path parameter names for nested routes https://chibisov.github.io/drf-extensions/docs/#nested-routes
            "PREPROCESSING_HOOKS": [
                "drf_spectacular_jsonapi.hooks.fix_nested_path_parameters",
            ],
        }

    # FILES
    FILE_UPLOAD_PERMISSIONS = 0o777
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777
    FILE_UPLOAD_HANDLERS = [
        "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    ]
    DIRECTORY = ""

    @classmethod
    def setup(cls) -> None:
        super().setup()
        if cls.FIX_RELATIVE_URLS:
            cls._fix_relative_urls()

    @classmethod
    def post_setup(cls) -> None:
        super().post_setup()
        logging.basicConfig(level=logging.INFO, format="*** %(message)s")
        cls.log.info("Starting %s project using %s configuration", cls.PROJECT_NAME, cls.__name__)

    @classmethod
    def _fix_relative_urls(cls) -> None:
        for url_attr in ("STATIC_URL", "MEDIA_URL"):
            url: str = getattr(cls, url_attr)
            if url.startswith("/"):
                url = urljoin(cls.PROJECT_BASE_URL, url)
            if not url.endswith("/"):
                url = f"{url}/"
            setattr(cls, url_attr, url)
