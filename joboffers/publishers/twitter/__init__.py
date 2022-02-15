import logging

import tweepy
from django.conf import settings

from joboffers.publishers import Publisher

ERROR_LOG_MESSAGE = 'Falló al querer publicar a twitter, data=%s: %s'


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
            api.update_status(message)
        except Exception as err:
            status = None
            logging.error(ERROR_LOG_MESSAGE, message, err)
        else:
            status = 200

        return status
