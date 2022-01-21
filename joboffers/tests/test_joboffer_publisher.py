import pytest
import requests
from django.template import Template, Context
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publisher import FacebookPublisher, Publisher, publish_offer
from ..models import OfferState
from .factories import JobOfferFactory


DUMMY_TEMPLATE = "<h1>{job_offer.slug}</h1> <p>{job_offer.company.name}</p>"
DUMMY_PUBLISHER_NAME = 'DUMMY_PUBLISHER'
DUMMY_PUBLISHER_URL = 'http://examplepublsih.com'


class DummyPublisher(Publisher):
    """Model interface for a publisher class."""
    name = DUMMY_PUBLISHER_NAME
    published_count = 0

    @classmethod
    def publish(cls, job_offer):
        cls._render_offer(job_offer)
        # A real publisher should call an external API
        # and the publsh method should return either success or not
        # And show the error or success message if possible
        requests.post(DUMMY_PUBLISHER_URL)
        cls.published_count += 1
        return {'status': cls.RESULT_OK,
                'text': f'The publication was successfull at {DUMMY_PUBLISHER_URL}'}

    @classmethod
    def _render_offer(cls, job_offer):
        template = Template(DUMMY_TEMPLATE)
        context = Context({'job_offer': job_offer})
        return template.render(context)


@pytest.mark.django_db
def test_publish_offer(requests_mock: Mocker):
    """Test that the offer is send to the different publishers."""
    requests_mock.post(DUMMY_PUBLISHER_URL, json='', status_code=201)
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    try:
        publish_offer(joboffer, (DummyPublisher, DummyPublisher))
        assert DummyPublisher.published_count == 2
    except NoMockAddress:
        assert False, 'publish_offer raised an exception, wich means that the url is malformed.'
    finally:
        DummyPublisher.published_count == 0


@pytest.mark.django_db
def test_facebook_publisher():
    """Test that the offer is send to the facebook publishers."""
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    publish_offer(joboffer, (FacebookPublisher,))
