from unittest.mock import patch

from django.conf import settings
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publishers.facebook import (ERROR_LOG_MESSAGE, FACEBOOK_POST_URL,
                                   FacebookPublisher)

DUMMY_MESSAGE = 'message'
DUMMY_EXCEPTION_MESSAGE = 'Oops'
DUMMY_BAD_REQUEST_TEXT = 'This is bad'


class DummyRequest:
    status_code = 400
    text = DUMMY_BAD_REQUEST_TEXT


def test_publish_message_ok(requests_mock: Mocker):
    """Test that a requests made to the facebook api is ok."""
    requests_mock.post(FACEBOOK_POST_URL, json='', status_code=200)

    try:
        status = FacebookPublisher()._push_to_api('message', 'title')
    except NoMockAddress:
        assert False, 'publish_offer raised an exception, wich means that the url is malformed.'

    assert status == 200


@patch(
        'joboffers.publishers.facebook.requests.post',
        side_effect=Exception(DUMMY_EXCEPTION_MESSAGE)
    )
def test_publish_message_urlerror(mocked_object, caplog):
    """Test error handling of requests made to the facebook api when url does not exists."""
    status = FacebookPublisher()._push_to_api('message', 'title')
    payload = {
        'message': DUMMY_MESSAGE,
        'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
    }

    expected_error_message = ERROR_LOG_MESSAGE % (
                                                    FACEBOOK_POST_URL,
                                                    payload, DUMMY_EXCEPTION_MESSAGE
                                                )

    assert expected_error_message in caplog.text
    assert status is None


def test_publish_message_parameters_error(caplog):
    """Test error handling of requests made to the facebook api when some parameter is wrong."""

    with patch('joboffers.publishers.facebook.requests.post') as mocked_object:

        mocked_object.return_value = DummyRequest
        status = FacebookPublisher()._push_to_api('message', 'title')

    payload = {
        'message': DUMMY_MESSAGE,
        'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
    }

    expected_error_message = ERROR_LOG_MESSAGE % (
                                                    FACEBOOK_POST_URL,
                                                    payload, DUMMY_BAD_REQUEST_TEXT
                                                )

    assert expected_error_message in caplog.text
    assert status == 400
