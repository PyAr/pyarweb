import logging

import tweepy
from django.conf import settings

from joboffers.publishers import Publisher

ERROR_LOG_MESSAGE_AUTH = ('Falló al querer generar las siguientes credenciales para twitter'
                          ' TWITTER_CONSUMER_KEY: %s'
                          ' TWITTER_CONSUMER_SECRET: %s'
                          ' TWITTER_ACCESS_TOKEN: %s'
                          ' TWITTER_ACCESS_SECRET: %s'
                          ' Error: %s')

ERROR_LOG_MESSAGE_POST = ('Falló al querer twitear con las siguientes credenciales.'
                          ' TWITTER_CONSUMER_KEY: %s'
                          ' TWITTER_CONSUMER_SECRET: %s'
                          ' TWITTER_ACCESS_TOKEN: %s'
                          ' TWITTER_ACCESS_SECRET: %s'
                          ' Error: %s')

ERROR_LOG_MESSAGE_GENERIC = 'Falló al querer publicar a twitter, data=%s: %s'


class TwitterPublisher(Publisher):
    """Twitter Publisher."""
    name = 'Twitter'

    def _push_to_api(self, message: str):
        """Publish a message to twitter."""

        try:
            auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                       settings.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)
            api = tweepy.API(auth)
        except Exception as err:
            status = None
            # Need to convert to string, in case they are strings or they are not set
            logging.error(ERROR_LOG_MESSAGE_AUTH,
                          str(settings.TWITTER_CONSUMER_KEY),
                          str(settings.TWITTER_CONSUMER_SECRET),
                          str(settings.TWITTER_ACCESS_TOKEN),
                          str(settings.TWITTER_ACCESS_SECRET),
                          err)
            return status

        try:
            api.update_status(message)
        except tweepy.errors.Unauthorized as err:
            # Specifically cacthing this exception as it could be helpful to debug errors on
            # this end.
            status = 401
            logging.error(ERROR_LOG_MESSAGE_POST,
                          settings.TWITTER_CONSUMER_KEY,
                          settings.TWITTER_CONSUMER_SECRET,
                          settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_SECRET,
                          err)
        except Exception as err:
            status = None
            logging.error(ERROR_LOG_MESSAGE_POST,
                          settings.TWITTER_CONSUMER_KEY,
                          settings.TWITTER_CONSUMER_SECRET,
                          settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_SECRET,
                          err)
        else:
            status = 200

        return status
