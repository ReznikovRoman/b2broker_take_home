from .base import Base


class CI(Base):
    PROJECT_ENVIRONMENT = "ci"

    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    SECRET_KEY = "xxx"  # noqa: S105
