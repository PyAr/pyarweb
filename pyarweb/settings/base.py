"""
Django settings for pyarweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# Dos veces os.path.dirname porque el archivo de settings está dentro de otro path.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', "somethingverysecret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Sites framework
SITE_ID = 1

ALLOWED_HOSTS = ['*']

# Django registration
# https://django-registration.readthedocs.org/en/latest/quickstart.html
ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'webmaster@python.org.ar'
LOGIN_REDIRECT_URL = '/'


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
    'joboffers',
    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    'taggit',
    'taggit_autosuggest',
    'pagination',
    'tagging',
    'bootstrap3',
    'django_summernote',
    'sendfile',
    'crispy_forms',
    'email_obfuscator',
    'dbbackup',
    'captcha',
    'sanitizer',
    'easyaudit'
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware'
)

ROOT_URLCONF = 'pyarweb.urls'

WSGI_APPLICATION = 'pyarweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', os.environ.get("POSTGRES_DB", "pyarweb")),
        'USER': os.environ.get('DB_USER', os.environ.get("POSTGRES_USER", "postgres")),
        'PASSWORD': os.environ.get('DB_PASS', os.environ.get("POSTGRES_PASSWORD", "")),
        'HOST': os.environ.get('DB_SERVICE', os.environ.get("POSTGRES_HOST", "localhost")),
        'PORT': int(os.environ.get('DB_PORT', os.environ.get("POSTGRES_PORT", 5432))),
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

PYAR_WIKI_URL = 'http://localhost:8080/pages/inicio'

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
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                'django.template.context_processors.static',
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "community.context_processors.pyar_wiki_url",

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

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SUMMERNOTE_CONFIG = {
    'inplacewidget_external_css': (),
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SENDFILE_BACKEND = 'sendfile.backends.simple'


# django-db backups
DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_BACKUP_DIRECTORY = os.path.join(BASE_DIR, '_backups')

#
# Events inscription captcha
#
CAPTCHA_LENGTH = 6
CAPTCHA_FLITE_PATH = "/usr/bin/flite"
CAPTCHA_IMAGE_TEMPLATE = "account/custom_captcha.html"

ALLOWED_HTML_TAGS_INPUT = [
    'a', 'b', 'br', 'i', 'u', 'p', 'hr',
    'pre', 'img', 'span', 'table', 'tbody',
    'thead', 'tr', 'th', 'td', 'blockquote',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'font',
    'o:p', 'sup', 'sub', 'strike', 'li', 'ul',
    'ol', 'div',
]
ALLOWED_HTML_ATTRIBUTES_INPUT = [
    'href', 'src', 'style', 'width', 'class', 'face',
]
ALLOWED_HTML_STYLES_INPUT = [
    'text-align', 'margin-left', 'background-color',
    'font-size',
]
TAGGIT_CASE_INSENSITIVE = True

GOOGLE_TRACKING_ID = os.environ.get('GOOGLE_TRACKING_ID', '')

ACCOUNT_FORMS = {
    'signup': 'pyarweb.forms.SingupFormWithCaptcha'
}

DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False

DJANGO_EASY_AUDIT_REGISTERED_CLASSES = ['joboffers.JobOffer', 'joboffers.JobofferComment']

# Azure blob-storage
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER")
AZURE_SSL = os.environ.get("AZURE_SSL", True)
AZURE_QUERYSTRING_AUTH = os.environ.get("AZURE_QUERYSTRING_AUTH", False)


# Telegram constants
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_MODERATORS_CHAT_ID = os.environ.get('TELEGRAM_MODERATORS_CHAT_ID')

# Facebook constants
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')

# Twitter constants
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
