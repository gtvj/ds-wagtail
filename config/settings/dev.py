from .base import *  # noqa: F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "True"))
DEBUG_TOOLBAR_ENABLED = strtobool(os.getenv("DEBUG_TOOLBAR_ENABLED", "True"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@6gce61jt^(pyj5+l**&*_#zyxfj5v1*71cs5yoetg-!fsz826"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *  # noqa: F401
except ImportError:
    pass

if DEBUG:
    LOGGING["root"]["level"] = "DEBUG"

if DEBUG and DEBUG_TOOLBAR_ENABLED:
    from .base import INSTALLED_APPS, LOGGING, MIDDLEWARE

    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
