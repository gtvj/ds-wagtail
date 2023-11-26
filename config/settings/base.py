"""
Django settings for etna project.

Generated by 'django-admin startproject' using Django 3.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os

from distutils.sysconfig import get_python_lib
from distutils.util import strtobool

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from ..versioning import get_git_sha

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = strtobool(os.getenv("DEBUG", "False"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "etna.generic_pages",
    "etna.alerts",
    "etna.analytics",
    "etna.articles",
    "etna.authors",
    "etna.categories",
    "etna.ciim",
    "etna.collections",
    "etna.core",
    "etna.feedback",
    "etna.highlights",
    "etna.home",
    "etna.images",
    "etna.media",
    "etna.navigation",
    "etna.records",
    "etna.search",
    "etna.users",
    "etna.whatson",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtailfontawesomesvg",
    "wagtailmedia",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "generic_chooser",
    "wagtailmetadata",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "birdbath",
]

SITE_ID = 1

MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "etna.core.middleware.MaintenanceModeMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "etna.core.middleware.InterpretCookiesMiddleware",
]

COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "nationalarchives.gov.uk")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(
                get_python_lib(), "nationalarchives-frontend-django/templates"
            ),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "etna.core.context_processors.feature_flags",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# django-allauth configuration
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = False  # Bypass logout confirmation form
ACCOUNT_USERNAME_REQUIRED = False  # Register using email only
ACCOUNT_SESSION_REMEMBER = False  # True|False disables "Remember me?" checkbox"
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/"
WAGTAIL_FRONTEND_LOGIN_URL = LOGIN_URL
# View access control
IMAGE_VIEWER_REQUIRE_LOGIN = strtobool(os.getenv("IMAGE_VIEWER_REQUIRE_LOGIN", "True"))
RECORD_DETAIL_REQUIRE_LOGIN = strtobool(
    os.getenv("RECORD_DETAIL_REQUIRE_LOGIN", "True")
)
SEARCH_VIEWS_REQUIRE_LOGIN = strtobool(os.getenv("SEARCH_VIEWS_REQUIRE_LOGIN", "True"))
# Custom adapter to prevent self-signup
ACCOUNT_ADAPTER = "etna.users.adapters.NoSelfSignupAccountAdapter"
ACCOUNT_FORMS = {"login": "etna.users.forms.EtnaLoginForm"}

WSGI_APPLICATION = "config.wsgi.application"

# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

SENTRY_DEBUG_URL_ENABLED = False
if SENTRY_DSN := os.getenv("SENTRY_DSN", ""):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=os.getenv("SENTRY_ENVIRONMENT", ""),
        release=get_git_sha(),
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", "0.5")),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=strtobool(os.getenv("SENTRY_SEND_USER_DATA", "False")),
    )

    SENTRY_DEBUG_URL_ENABLED = strtobool(os.getenv("SENTRY_DEBUG_URL_ENABLED", "False"))


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DATABASE_NAME", "db.sqlite3"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "templates", "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Should always be False in production. Can be set to True in local environments
# to serve static files even when DEBUG is False
DJANGO_SERVE_STATIC = False

WAGTAILMEDIA = {
    "MEDIA_MODEL": "media.EtnaMedia",
    "MEDIA_FORM_BASE": "etna.media.forms.BaseMediaForm",
}

# Wagtail settings

WAGTAIL_SITE_NAME = "etna"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.getenv("WAGTAILADMIN_BASE_URL", "https://www.example.com")

# For search results within Wagtail itself
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"

# Custom password template for private pages

PASSWORD_REQUIRED_TEMPLATE = "password_pages/password_required.html"

# Eventbrite client

EVENTBRITE_KEY = os.getenv("EVENTBRITE_KEY")
EVENTBRITE_SECRET = os.getenv("EVENTBRITE_SECRET")
EVENTBRITE_PRIVATE_TOKEN = os.getenv("EVENTBRITE_PRIVATE_TOKEN")
EVENTBRITE_PUBLIC_TOKEN = os.getenv("EVENTBRITE_PUBLIC_TOKEN")
EVENTBRITE_ORGANIZER_ID = os.getenv("EVENTBRITE_ORGANIZER_ID")
EVENTBRITE_TNA_ORGANISATION_ID = os.getenv("EVENTBRITE_TNA_ORGANISATION_ID")

# API Client

CLIENT_BASE_URL = os.getenv("KONG_CLIENT_BASE_URL")
CLIENT_KEY = os.getenv("KONG_CLIENT_KEY")
CLIENT_VERIFY_CERTIFICATES = strtobool(
    os.getenv("KONG_CLIENT_VERIFY_CERTIFICATES", "True")
)
IMAGE_PREVIEW_BASE_URL = os.getenv("KONG_IMAGE_PREVIEW_BASE_URL")

# Rich Text Features
# https://docs.wagtail.io/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field
INLINE_RICH_TEXT_FEATURES = [
    "bold",
    "italic",
    "link",
]
RESTRICTED_RICH_TEXT_FEATURES = INLINE_RICH_TEXT_FEATURES + [
    "ol",
    "ul",
]
EXPANDED_RICH_TEXT_FEATURES = RESTRICTED_RICH_TEXT_FEATURES + [
    "h2",
    "h3",
]

# Analytics
AVAILABILITY_CONDITION_CATEGORIES = {
    "AcademicSubscription": "Academic Subscription",
    "AccessUnderReview": "Not Viewable online",
    "AV_Media": "Viewable online",
    "ClosedFOIReview": "Not viewable online",
    "ClosedRetainedDeptKnown": "Not viewable online",
    "ClosedRetainedDeptUnKnown": "Not viewable online",
    "CollectionCare": "Not viewable online",
    "DigitizedAvailableButNotDownloadableAtItemLevel": "Not viewable online",
    "DigitizedAvailableButNotDownloadableAtPieceLevel": "Not viewable online",
    "DigitizedDiscovery - Free": "Viewable online",
    "DigitizedDiscovery - Charged": "Viewable online",
    "DigitizedDiscovery - Charged (+LIAs)": "Viewable online & via 3rd party",
    "DigitizedLIA": "Viewable via 3rd party",
    "DigitizedOther": "Viewable online",
    "DigitizedPartiallyOpened": "Not used",
    "DisplayAtMuseum": "Not viewable online",
    "FileAuthority": "Not viewable online",
    "GovtWebArchive": "Viewable via 3rd party",
    "ImageLibrary": "Viewable via 3rd party",
    "InUse": "Not viewable online",
    "InvigilationSafeRoom": "Not viewable online",
    "LocalArchive": "Not viewable online",
    "MissingLost": "Not viewable online",
    "MouldTreatment": "Not viewable online",
    "Offsite": "Not viewable online",
    "Onloan": "Not viewable online",
    "OrderException": "Error",
    "OrderOriginal": "Not viewable online",
    "PaidSearch": "Not viewable online",
    "Surrogate": "Not viewable online",
    "TooLargeToCopyOffsite": "Not viewable online",
    "TooLargeToCopyOriginal": "Not viewable online",
    "TooLargeToCopySurrogate": "Not viewable online",
    "Unavailable": "Not viewable online",
    "Unfit": "Not viewable online",
}

# Don't anonymise data by default, so we don't accidentally lose production data
BIRDBATH_REQUIRED = False
BIRDBATH_PROCESSORS = ["etna.users.anonymisation.UserAnonymiser"]

# -----------------------------------------------------------------------------
# Default cache-control settings
# -----------------------------------------------------------------------------

# Set s-max-age header that is used by reverse proxy/front end cache.
# See core.cache_control.get_default_cache_control_kwargs()
# The default value is 3 hours.
try:
    CACHE_CONTROL_S_MAXAGE = int(os.getenv("CACHE_CONTROL_S_MAXAGE", 60 * 60 * 3))
except ValueError:
    pass

# Give front-end cache 30 second to revalidate the cache to avoid hitting the backend.
# See core.cache_control.get_default_cache_control_kwargs()
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    os.getenv("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)

# -----------------------------------------------------------------------------
# Maintenance mode
# -----------------------------------------------------------------------------

MAINTENANCE_MODE = strtobool(os.getenv("MAINTENANCE_MODE", "False"))
# MAINTENENCE_MODE_ALLOW_IPS="IPA1,IPA2" where IPA is IP address
MAINTENENCE_MODE_ALLOW_IPS = os.getenv("MAINTENENCE_MODE_ALLOW_IPS", "").split(",")
# datetime is iso MAINTENENCE_MODE_ENDS = "2011-11-04T00:05:23+04:00"
MAINTENENCE_MODE_ENDS = os.getenv("MAINTENENCE_MODE_ENDS", "")

# -----------------------------------------------------------------------------
# Feature flags
# -----------------------------------------------------------------------------

# Special boolean settings prefixed with 'FEATURE_', that are automatically
# injected into template contexts using a custom context processor - allowing
# conditional logic to be added to both Python and template code

FEATURE_RECORD_LINKS_GO_TO_DISCOVERY = strtobool(
    os.getenv("FEATURE_RECORD_LINKS_GO_TO_DISCOVERY", "False")
)
FEATURE_DOWNLOAD_RECORD_LINKS_GO_TO_DISCOVERY = strtobool(
    os.getenv("FEATURE_DOWNLOAD_RECORD_LINKS_GO_TO_DISCOVERY", "False")
)
FEATURE_BETA_BANNER_ENABLED = strtobool(
    os.getenv("FEATURE_BETA_BANNER_ENABLED", "True")
)
FEATURE_COOKIE_BANNER_ENABLED = strtobool(
    os.getenv("FEATURE_COOKIE_BANNER_ENABLED", "True")
)
FEATURE_PLATFORM_ENVIRONMENT_TYPE = os.getenv("PLATFORM_ENVIRONMENT_TYPE", "production")
FEATURE_FEEDBACK_MECHANISM_ENABLED = strtobool(
    os.getenv("FEATURE_FEEDBACK_MECHANISM_ENABLED", "False")
)
FEATURE_DISABLE_JS_WHATS_ON_LISTING = strtobool(
    os.getenv("FEATURE_DISABLE_JS_WHATS_ON_LISTING", "False")
)
