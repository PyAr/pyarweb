import logging

from django.conf import settings
from mastodon import Mastodon, errors

from joboffers.utils import hash_secret
from joboffers.publishers import Publisher


def _repr_credentials():
    """Show a string representation of mastodon credentials."""
    # Need to convert to string, in case they are strings or they are not set
    credentials_repr = (
        f' MASTODON_AUTH_TOKEN: {hash_secret(settings.MASTODON_AUTH_TOKEN)} '
        f' MASTODON_API_BASE_URL: {hash_secret(settings.MASTODON_API_BASE_URL)} '
    )
    return credentials_repr


ERROR_LOG_MESSAGE = (
    'Falló al querer tootear con las siguientes credenciales (hasheadas): %s - Error: %s'
)


class MastodonPublisher(Publisher):
    """Mastodon Publisher."""

    name = 'Mastodon'

    def _push_to_api(self, message: str, title: str, link: str):
        """Publish a message to mastodon."""
        mastodon = Mastodon(
            access_token=settings.MASTODON_AUTH_TOKEN,
            api_base_url=settings.MASTODON_API_BASE_URL,
        )

        try:
            mastodon.status_post(message)
        except errors.MastodonUnauthorizedError as err:
            status = None
            logging.error(ERROR_LOG_MESSAGE, _repr_credentials(), err)
        except Exception as err:
            status = None
            logging.error("Unknown error when tooting: %s", repr(err))
        else:
            status = 200

        return status
