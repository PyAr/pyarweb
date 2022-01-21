import requests

from .models import JobOffer

PAGE_ID = xxxxx
FACEBOOK_TOKEN = 'EAAEivURMffgBAKNT'


class Publisher:
    """Abstract class for Publishing classes like Twitter, Facebook, etc."""
    name = None
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        raise NotImplementedError

    @classmethod
    def _render_offer(cls, job_offer: 'JobOffer'):
        raise NotImplementedError


def publish_offer(job_offer: 'JobOffer', publishers: list = None):
    """Publish a job_offer into the given list of publishers."""
    results = {}

    if publishers:
        for publisher in publishers:
            results[publisher.name] = publisher.publish(job_offer)
    else:
        raise ValueError

    return results


# Tutorial for facebook publish on page
# https://medium.com/nerd-for-tech/automate-facebook-posts-with-python-and-facebook-graph-api-858a03d2b142

class FacebookPublisher:
    """Facebook Publisher."""
    name = 'Facebook'
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        msg = 'Probando API'
        post_url = 'https://graph.facebook.com/{}/feed'.format(PAGE_ID)
        payload = {
        'message': msg,
        'access_token': FACEBOOK_TOKEN
        }
        breakpoint()
        r = requests.post(post_url, data=payload)
        pass

    @classmethod
    def _render_offer(cls, job_offer: 'JobOffer'):
        raise NotImplementedError



