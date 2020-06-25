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
    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
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
    'captcha',
    'email_confirm_la',
    'sanitizer',
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
        'NAME': os.environ.get('DB_NAME', os.environ.get("POSTGRES_DB", "pyarweb")),
        'USER': os.environ.get('DB_USER', os.environ.get("POSTGRES_USER", "postgres")),
        'PASSWORD': os.environ.get('DB_PASS', os.environ.get("POSTGRES_PASSWORD", "")),
        'HOST': os.environ.get('DB_SERVICE', os.environ.get("POSTGRES_HOST", "localhost")),
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
                "django.core.context_processors.debug",
                "django.core.context_processors.media",
                'django.core.context_processors.static',
                "django.core.context_processors.request",
                "django.core.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "planet.context_processors.context",
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
#  Email confirmation app settings
#
EMAIL_CONFIRM_LA_DOMAIN = "python.org.ar"
EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 3600*24*7  # 7 días
EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT = {
    'confirmation_url_validity_time': EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC / (
        3600*24),  # days
}

#
# Events inscription captcha
#
CAPTCHA_LENGTH = 6

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
