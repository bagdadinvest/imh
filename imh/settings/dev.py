from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "-9ds5tf^9o=@w^59npt@s#d)u!$b$m30ez+e$1*b9m@4(!=bh)"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://istanbulmasajhotel.com",  # Add your domain here
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass
