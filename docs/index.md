# How to review this project
The project description can be found in the [README](../README.md). Below is a short instruction for a quick review.

0. Clone the repository
```shell
git clone https://github.com/ReznikovRoman/b2broker_take_home.git && cd b2broker_take_home
```

1. Configure environment variables in `.env` file.
```shell
cat << EOF > .env
ENV=.env
PYTHONUNBUFFERED=1
DJANGO_SETTINGS_MODULE=b2broker.settings
DJANGO_CONFIGURATION=Local
DJANGO_ADMIN=django-cadmin
SECRET_KEY=ep5((kb0ia=w4^bel4m!s4z)77+fp&-.xeieg*k).%t+x&g=01
ALLOWED_HOSTS=localhost,127.0.0.1
B2B_PROJECT_BASE_URL=http://localhost:8000
B2B_MEDIA_URL=/media/
B2B_STATIC_URL=/staticfiles/
B2B_DB_HOST=db
B2B_DB_PORT=3306
B2B_DB_NAME=b2broker
B2B_DB_USER=roman
B2B_DB_PASSWORD=pswd
B2B_CI=0
EOF
```

2. Create new settings file for local development `b2broker/settings/local.py`. For example:
```shell
cat << EOF > b2broker/settings/local.py
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
EOF
```

3. Start docker containers
```shell
docker-compose build
docker-compose up -d
```

4. Go to the admin panel for authentication `http://localhost:8000/admin/`.
Credentials are specified in the docker compose:
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=pass
```

5. Go to [Swagger for reviewing API](http://localhost:8000/api/v1/schema/swagger#/)

6. After review you can stop the containers and remove associated data
```shell
docker-compose down -v --remove-orphans --rmi local
```
