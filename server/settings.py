"""Settings module"""

from pathlib import Path
import os

VERSION = "0.11.0-nightly.0"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
GDAL_LIBRARY_PATH = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ginger-insecure-u0j2maaxfoo8t1_l(l*asol9gw@(we8j=_lkn9m$dla55^(74@"

JWT_SECRET_KEY = os.getenv("JWT_SECRET", "1234")

DEV_DEFAULT_ID = "db-compose-test-env"

APP_ID = os.getenv("APP_ID", "db-compose-test-env")
ADDITIONAL_TEMPLATES_FOLDER = os.getenv("ADDITIONAL_TEMPLATES_FOLDER")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.getenv("HOST", "localhost"), "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("HOST", "localhost")]
CORS_ALLOWED_ORIGINS = ["https://" + os.getenv("HOST", "localhost")]

# Application definition

INSTALLED_APPS = [
    "gingerdj.contrib.admin",
    "gingerdj.contrib.messages",
    "gingerdj.contrib.staticfiles",
    "gingerdj.rest_framework",
    "gingerdj.drf_yasg",
    "gingerdj.prometheus",
    "src",
]

MIDDLEWARE = [
    "gingerdj.middleware.security.SecurityMiddleware",
    "gingerdj.contrib.sessions.middleware.SessionMiddleware",
    "gingerdj.middleware.common.CommonMiddleware",
    "gingerdj.middleware.csrf.CsrfViewMiddleware",
    "gingerdj.contrib.messages.middleware.MessageMiddleware",
    "gingerdj.middleware.clickjacking.XFrameOptionsMiddleware",
]

if APP_ID != DEV_DEFAULT_ID:
    MIDDLEWARE.append("server.middlewares.JWTAuthMiddleware")

ROOT_URLCONF = "server.urls"

TEMPLATES_DIR = [
    os.path.join(BASE_DIR, "src", "orm_templates", "ts"),
    os.path.join(BASE_DIR, "src", "orm_templates"),
    os.path.join(BASE_DIR, "src", "templates"),
]
# Only add ADDITIONAL_TEMPLATES_FOLDER if it's set
if ADDITIONAL_TEMPLATES_FOLDER:
    TEMPLATES_DIR.append(os.path.join(BASE_DIR, "src", ADDITIONAL_TEMPLATES_FOLDER))

TEMPLATES = [
    {
        "BACKEND": "gingerdj.template.backends.gingerdj.GingerTemplates",
        "DIRS": TEMPLATES_DIR,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "gingerdj.template.context_processors.debug",
                "gingerdj.template.context_processors.request",
                "gingerdj.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

if not os.getenv("DB_NAME"):
    print("Using SQLite3")
    DATABASES = {
        "default": {
            "ENGINE": "gingerdj.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("Using PostgreSQL")
    DATABASES = {  # pragma: no cover
        "default": {
            "ENGINE": "gingerdj.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("DB_NAME", "db"),
            "USER": os.getenv("DB_USERNAME", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "gingerdj.db.models.BigAutoField"

STATICFILES_DIRS = [
    BASE_DIR / "static",  # BASE_DIR is your project root
]


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "BearerAuth": {"type": "apiKey", "name": "Authorization", "in": "header"},
        "BearerAPIAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Authorization",
        },
    },
}
