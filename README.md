# B2Broker
Crypto wallet management app for B2Broker.

## Configuration
Docker containers::
1. db
2. server

docker-compose files:
 1. `docker-compose.yml` - for local development.

To run docker containers, you need to create a `.env` file in the root directory.

**`.env` file format:**
```dotenv
ENV=.env

# Python
PYTHONUNBUFFERED=1

# B2Broker
# Django
DJANGO_SETTINGS_MODULE=b2broker.settings
DJANGO_CONFIGURATION=Local
DJANGO_ADMIN=django-cadmin
SECRET_KEY=ep5((kb0ia=w4^bel4m!s4z)77+fp&-.xeieg*k).%t+x&g=01
ALLOWED_HOSTS=localhost,127.0.0.1

# Project
B2B_PROJECT_BASE_URL=http://localhost:8000

# Media
B2B_MEDIA_URL=/media/
B2B_STATIC_URL=/staticfiles/

# MySQL
B2B_DB_HOST=db
B2B_DB_PORT=3306
B2B_DB_NAME=b2broker
B2B_DB_USER=user
B2B_DB_PASSWORD=pswd

# Config
B2B_CI=0
```

To run project locally, you need to create local Django settings `b2broker/settings/local.py`:
```python
import mimetypes
import socket

from .base import Base
from .values import from_environ


class Local(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]

    STATIC_URL = "staticfiles/"

    LOG_SQL = from_environ(False, name="PROJECT_LOG_SQL", type=bool)

    # debug toolbar
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda show_toolbar: True,
    }
    mimetypes.add_type("application/javascript", ".js", True)

    DEV_INSTALLED_APPS = [
        "debug_toolbar",
    ]
    DEV_MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    Base.INSTALLED_APPS.extend(DEV_INSTALLED_APPS)
    Base.MIDDLEWARE.extend(DEV_MIDDLEWARE)
```

Superuser credentials for the admin panel are configured in docker compose:
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=pass
```

You can access the site itself by visiting http://localhost:8000/admin

**Start project:**
```shell
docker-compose build
docker-compose up
```

On startup migrations are applied and static files are collected.

## Development
In this project [`django-configurations`](https://django-configurations.readthedocs.io/en/latest/) is configured,
therefore for running management commands instead of using `./manage.py` / `python -m django` / `django-admin`
you have to use `django-cadmin`.

**Example: Creating a superuser**
```shell
django-cadmin createsuperuser
```

Sync environment with `requirements.txt` / `requirements.dev.txt` (will install/update missing packages, remove redundant ones):
```shell
make sync-requirements
```

Compile requirements.\*.txt files (have to re-compile after changes in requirements.\*.in):
```shell
make compile-requirements
```

Use `requirements.local.in` for local dependencies; always specify _constraints files_ (-c ...)

Example:
```shell
# requirements.local.txt

-c requirements.txt
-c requirements.dev.txt

ipython
```


### Code style:
Configure pre-commit locally:

```shell
pre-commit install
```

Before pushing a commit run all linters:

```shell
make lint
```

Automatically resolve linter errors:

```shell
make fix
```

## Documentation
OpenAPI 3 documentation::

* `${PROJECT_BASE_URL}/api/v1/schema` - YAML or JSON, selection via content negotiation with the Accept header
* `${PROJECT_BASE_URL}/api/v1/schema/redoc` - ReDoc
* `${PROJECT_BASE_URL}/api/v1/schema/swagger` - Swagger UI
