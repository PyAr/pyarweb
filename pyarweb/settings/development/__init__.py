import os

from pyarweb.settings.base import *  # NOQA

# Instead of sending out real emails the console backend just writes
# the emails that would be sent to the standard output.
# By default, the console backend writes to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEBUG = True

# Prefix for telegram messages
TELEGRAM_MESSAGE_PREFIX = '[DEV]'

SOCIAL_NETWORKS_PUBLISHERS = []  # Empty by default to avoid sending on local testing

# BASE_URL to use in any notification that might require them
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')

DISCOURSE_HOST = "testdiscourse.com"
