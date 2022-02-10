from unittest.mock import patch

from django.conf import settings
from requests_mock.exceptions import NoMockAddress
from requests_mock.mocker import Mocker

from ..publishers.facebook import FACEBOOK_POST_URL, ERROR_LOG_MESSAGE, publish

DUMMY_MESSAGE = 'message'
DUMMY_EXCEPTION_MESSAGE= 'Oops'


def test_publish_message_ok(requests_mock: Mocker):
    """Test that a requests made to the facebook api is ok."""
    requests_mock.post(FACEBOOK_POST_URL, json='', status_code=200)

    try:
        status = publish('message')
    except NoMockAddress:
        assert False, 'publish_offer raised an exception, wich means that the url is malformed.'

    assert status == 200


@patch('joboffers.publishers.facebook.requests.post',
           side_effect=Exception(DUMMY_EXCEPTION_MESSAGE))
def test_publish_message_urlerror(mocked_object, caplog):
    """Test error handling of requests made to the facebook api when url does not exists."""
    status = publish('message')
    payload = {
        'message': DUMMY_MESSAGE,
        'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN
    }

    expected_error_message = ERROR_LOG_MESSAGE.format(FACEBOOK_POST_URL,
                                                      payload, DUMMY_EXCEPTION_MESSAGE)

    assert expected_error_message in caplog.text
    assert status == 500

