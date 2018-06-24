from pyarweb.settings.base import *  # NOQA


# Instead of sending out real emails the console backend just writes
# the emails that would be sent to the standard output.
# By default, the console backend writes to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEBUG = True
