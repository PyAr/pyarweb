"""
Django settings for pyarweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from datetime import timedelta
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', "somethingverysecret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Sites framework
SITE_ID = 1

ALLOWED_HOSTS = []

# Django registration
# https://django-registration.readthedocs.org/en/latest/quickstart.html
ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'webmaster@python.org.ar'
LOGIN_REDIRECT_URL = '/'


# Disqus
DISQUS_API_KEY = '3t6eKCbxRGuIG3SmdHb8malOf1h2WxSYEfXbBjWyNBaFLMyD1GOIfWYFciqJqo69'
DISQUS_WEBSITE_SHORTNAME = 'PyAr'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # pyarweb apps
    'community',
    'news',
    'pycompanies',
    'jobs',
    'events',
    'tutoring',

    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    # Ver esto mas adelante
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
    'django_extensions',
    'disqus',
    'taggit',
    'taggit_autosuggest',
    'bootstrap3_datetime',
    'planet',
    'pagination',
    'tagging',
    'bootstrap3',
    'django_summernote',
    'sendfile',
    'crispy_forms',
    'email_obfuscator',
    'dbbackup',
    'waliki',
    'waliki.git',
    'waliki.attachments',
    'waliki.slides',
    'waliki.togetherjs',
    'captcha',
    'email_confirm_la',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'pyarweb.urls'

WSGI_APPLICATION = 'pyarweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', "pyarweb"),
        'USER': os.environ.get('DB_USER', "postgres"),
        'PASSWORD': os.environ.get('DB_PASS', ""),
        'HOST': os.environ.get('DB_SERVICE', "localhost"),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Activa todo el sitio con el horario de Argentina
# from django.utils import timezone
# timezone.activate(TIME_ZONE)

USE_I18N = True

USE_L10N = True

USE_TZ = True

FORMAT_MODULE_PATH = 'pyarweb.formats'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'OPTIONS': {
            'context_processors': [
                #  allauth specific context processors
                # "allauth.account.context_processors.account",
                # "allauth.socialaccount.context_processors.socialaccount",

                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.media",
                'django.core.context_processors.static',
                "django.core.context_processors.request",
                "django.core.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "planet.context_processors.context",

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

PLANET = {"USER_AGENT": "pyarweb/0.1", "LOGIN_REQUIRED_FOR_ADDING_FEED": True}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SUMMERNOTE_CONFIG = {
    'inplacewidget_external_css': (),
}

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'update_feeds': {
        'task': 'planet.tasks.update_feeds',
        'schedule': timedelta(hours=12)
    },
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

WALIKI_INDEX_SLUG = 'Inicio'
WALIKI_AVAILABLE_MARKUPS = ['reStructuredText']
WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', )
WALIKI_LOGGED_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')
WALIKI_CODEMIRROR_SETTINGS = {'lineNumbers': True,
                              'theme': 'monokai',
                              'autofocus': True}
SENDFILE_BACKEND = 'sendfile.backends.simple'


# django-db backups
DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_BACKUP_DIRECTORY = os.path.join(BASE_DIR, '_backups')

RAVEN_CONFIG = None

#
#  Email confirmation app settings
#
EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 3600*24*7  # 7 días
EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT = {
    'confirmation_url_validity_time': EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC / (3600*24),  # days
}

#
# Events inscription captcha
#
CAPTCHA_LENGTH = 6


try:
    from .local_settings import *
except:
    pass

try:
    from .devsettings import *
except:
    pass

# Instead of sending out real emails the console backend just writes
# the emails that would be sent to the standard output.
# By default, the console backend writes to stdout
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if RAVEN_CONFIG:
    INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)
