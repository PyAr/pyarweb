import os
import sys

from pyarweb.settings.base import *  # NOQA

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'pyarweb_cache',
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/code/static2/'
STATIC_URL = '/static/'

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[PyAr]"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '587')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_TIMEOUT = int(os.environ.get('EMAIL_TIMEOUT', '10'))
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'do_not_reply@python.org.ar')

PYAR_WIKI_URL = 'https://wiki.staging.python.org.ar'

SENDFILE_BACKEND = "sendfile.backends.nginx"
SENDFILE_ROOT = '/home/www-pyar/pyarweb/pyarweb/media/waliki_attachments/'
SENDFILE_URL = '/private'

DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"

# Raven
# True if we are running ./manage.py test
TEST_RUNNING = [x for x in sys.argv if 'test' in x]

if not TEST_RUNNING:
    # Este es un workaround para evitar que unitests.discover importe el modulo y ejecute
    # raven.
    # Mejores maneras de evitar esto bienvenidas.
    import raven
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',) # NOQA
    RAVEN_CONFIG = {
            'dsn': os.environ.get("SENTRY_DSN", "NOT_CONFIGURED"),
            'release': raven.fetch_git_sha(BASE_DIR),  # NOQA
    }
