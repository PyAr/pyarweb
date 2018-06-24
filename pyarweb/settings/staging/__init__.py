import os
import sys

from pyarweb.settings.base import *  # NOQA

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'pyarweb_cache',
    }
}

ALLOWED_HOSTS = ['www.python.org.ar']

STATIC_ROOT = '/home/www-pyar/pyarweb/static/'
STATIC_URL = '/static/'

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[PyAr]"
EMAIL_CONFIRM_LA_DOMAIN = "python.org.ar"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'pyarweb@python.org.ar'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

# Disqus
DISQUS_API_KEY = os.environ.get("DISQUS_API_KEY", 'not_configured')
DISQUS_WEBSITE_SHORTNAME = 'PyAr'

# WALIKI
WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', )
WALIKI_COMMITER_NAME = 'PyArense Anónimo'

SENDFILE_BACKEND = "sendfile.backends.nginx"
SENDFILE_ROOT = '/home/www-pyar/pyarweb/pyarweb/media/waliki_attachments/'
SENDFILE_URL = '/private'

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
