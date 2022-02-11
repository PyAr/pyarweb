import tweepy
from django.conf import settings


ERROR_LOG_MESSAGE = 'Falló al querer publicar a twitter, data={}: {}'


def publish(message: str):
    """Publish a message to the configured facebook page."""

    try:
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(message)
    except Exception as err:
        status=500
        logging.error(ERROR_LOG_MESSAGE.format(ERROR_LOG_MESSAGE, message, err))
    else:
        status=200

    return status


class TwitterPublisher(Publisher):
    """Twitter Publisher."""
    name = 'Twitter'
    publish_method = publish
