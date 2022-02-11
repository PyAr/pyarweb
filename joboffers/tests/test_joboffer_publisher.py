from unittest.mock import patch

import pytest
import requests
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publishers import Publisher, publish_offer
from ..models import OfferState
from .factories import JobOfferFactory


DUMMY_PUBLISHER_NAME = 'DUMMY_PUBLISHER'
DUMMY_PUBLISHER_URL = 'http://examplepublsih.com'


class DummyPublisher(Publisher):
    """Model interface for a publisher class."""
    name = DUMMY_PUBLISHER_NAME
    published_count = 0

    def publish(self, job_offer):
        requests.post(DUMMY_PUBLISHER_URL)
        DummyPublisher.published_count += 1
        return {'status': self.RESULT_OK,
                'text': f'The publication was successfull at {DUMMY_PUBLISHER_URL}'}


@pytest.mark.django_db
def test_publish_offer(requests_mock: Mocker):
    """Test that the offer is sent to the different publishers."""
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
def test_rendering():
    """Test template_rendering."""
    job_offer = JobOfferFactory.create(state=OfferState.DEACTIVATED)
    result = Publisher()._render_offer(job_offer)
    assert result == f'<h1>New job!: { job_offer.slug }</h1>\n'


@pytest.mark.django_db
def test_publisher_publish_ok():
    """Test calling to publisher method without errors."""
    job_offer = JobOfferFactory.create(state=OfferState.DEACTIVATED)
    with patch('joboffers.publishers.Publisher._push_to_api') as mocked_publish:
        mocked_publish.return_value = 200
        result = Publisher().publish(job_offer)

    assert result == Publisher.RESULT_OK


@pytest.mark.django_db
def test_publisher_publish_error():
    """Test calling to publisher method and handling of errors."""
    job_offer = JobOfferFactory.create(state=OfferState.DEACTIVATED)
    with patch('joboffers.publishers.Publisher._push_to_api') as mocked_publish:
        mocked_publish.return_value = 400
        result = Publisher().publish(job_offer)

    assert result == Publisher.RESULT_BAD
