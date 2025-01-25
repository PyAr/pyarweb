import logging

import tweepy
from django.conf import settings

from joboffers.utils import hash_secret
from joboffers.publishers import Publisher


def _repr_credentials():
    """Show a string representation of twitter credentials."""
    # Need to convert to string, in case they are strings or they are not set
    credentials_repr = (
        f' TWITTER_CONSUMER_KEY: {hash_secret(settings.TWITTER_CONSUMER_KEY)} '
        f' TWITTER_CONSUMER_SECRET: {hash_secret(settings.TWITTER_CONSUMER_SECRET)} '
        f' TWITTER_ACCESS_TOKEN: {hash_secret(settings.TWITTER_ACCESS_TOKEN)} '
        f' TWITTER_ACCESS_SECRET: {hash_secret(settings.TWITTER_ACCESS_SECRET)} '
    )

    return credentials_repr


ERROR_LOG_MESSAGE_AUTH = (
    'Falló al querer autenticar con las siguientes credenciales(hasheadas)'
    'para twitter %s Error: %s'
)

ERROR_LOG_MESSAGE_POST = (
    'Falló al querer twitear con las siguientes credenciales(hasheadas). %s Error: %s'
)

ERROR_LOG_MESSAGE_GENERIC = 'Falló al querer publicar a twitter, data=%s: %s'


class TwitterPublisher(Publisher):
    """Twitter Publisher."""

    name = 'Twitter'

    def _push_to_api(self, message: str, title: str, link: str):
        """Publish a message to twitter."""
        try:
            auth = tweepy.OAuthHandler(
                settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET
            )
            auth.set_access_token(
                settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET
            )
            api = tweepy.API(auth)
        except TypeError as err:
            logging.error(err)
            return
        except Exception as err:
            logging.error(ERROR_LOG_MESSAGE_AUTH, _repr_credentials(), err)
            return

        try:
            api.update_status(message)
        except tweepy.errors.Unauthorized as err:
            # Specifically cacthing this exception as it could be helpful to debug errors on
            # this end.
            status = 401
            logging.error(ERROR_LOG_MESSAGE_POST, _repr_credentials(), err)
        except Exception as err:
            status = None
            logging.error(ERROR_LOG_MESSAGE_POST, _repr_credentials(), err)
        else:
            status = 200

        return status
