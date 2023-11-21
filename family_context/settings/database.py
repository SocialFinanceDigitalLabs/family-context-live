import dj_database_url
from decouple import config

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

MAX_CONN_AGE = 600
DATABASE_URL = config("DATABASE_URL", default=False)

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=MAX_CONN_AGE,
        ),
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            default="sqlite://{BASE_DIR}/db.sqlite3",
            conn_max_age=MAX_CONN_AGE,
            ssl_require=False,
        ),
    }