from unittest.mock import patch

import mastodon

from ..publishers.mastodon import MastodonPublisher

DUMMY_MESSAGE = 'message'
DUMMY_TITLE = 'title'
DUMMY_LINK = 'https://example.com'


class DummyAPIBad:
    def __init__(self, to_raise):
        self.to_raise = to_raise

    def status_post(self, *args, **kwargs):
        raise self.to_raise


class DummyAPIOK:
    def status_post(*args, **kwargs):
        return


@patch('joboffers.publishers.mastodon.Mastodon')
def test_push_to_api_bad_credentials(mock_api, settings, caplog):
    """Test exception when the credentials are wrong."""
    mock_api.return_value = DummyAPIBad(mastodon.errors.MastodonUnauthorizedError("bad auth"))
    settings.MASTODON_AUTH_TOKEN = "wrong"
    settings.MASTODON_API_BASE_URL = "creds"

    status = MastodonPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status is None

    expected_error_message = "Falló al querer tootear con las siguientes credenciales (hasheadas)"
    assert expected_error_message in caplog.text


@patch('joboffers.publishers.mastodon.Mastodon')
def test_push_to_api_generic_error(mock_api, settings, caplog):
    """Something went wrong."""
    mock_api.return_value = DummyAPIBad(ValueError("boom"))
    settings.MASTODON_AUTH_TOKEN = "good"
    settings.MASTODON_API_BASE_URL = "creds"

    status = MastodonPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status is None

    expected_error_message = "Unknown error when tooting: ValueError"
    assert expected_error_message in caplog.text


@patch('joboffers.publishers.mastodon.Mastodon')
def test_push_to_api_ok(mock_api, settings):
    mock_api.return_value = DummyAPIOK
    settings.MASTODON_AUTH_TOKEN = "good"
    settings.MASTODON_API_BASE_URL = "creds"

    status = MastodonPublisher()._push_to_api(DUMMY_MESSAGE, DUMMY_TITLE, DUMMY_LINK)
    assert status == 200
