from unittest.mock import MagicMock

from django.core import mail
from ..utils import hash_secret, normalize_tags, send_mail_to_publishers


def test_normalize_tags_with_repeated():
    """
    Test that uppercase/lowercase combinations be unified
    """
    repeated_tags = ['Django', 'DJANGO', 'djAngo']
    tags = normalize_tags(repeated_tags)
    assert len(tags) == 1


def test_normalize_tags_sorrunding_with_symbols_and_spaces():
    """
    Test that unwanted leading and trailing symbols be unified as one tag
    """
    repeated_tags = ['  Django', '@django ', '//DJANGO', '#django#']
    tags = normalize_tags(repeated_tags)
    assert len(tags) == 1


def test_normalize_tags_with_non_ascii():
    """
    Test normalizing non assci chars
    """
    repeated_tags = ['DñàÈ', ]
    tags = list(normalize_tags(repeated_tags))
    assert len(tags) == 1
    assert tags[0].islower()
    assert 'dnae' == tags[0]


def test_hash_secret():
    """
    Test hash_secret method. It should receive a string and return a sha256 hexdigest.
    """
    dummy_secret = 'kl^324523²#¹¹}##'
    expected_result = '787de9491332e7f258aadf90983101d0dfa63973a9ac935deb37cdea76bac1f3'
    result = hash_secret(dummy_secret)
    assert result == expected_result


def test_hash_secret_None():
    """
    Test hash_secret method when recieves None It should return 'None' as a string.
    """
    dummy_secret = None
    expected_result = 'None'
    result = hash_secret(dummy_secret)
    assert result == expected_result


TEST_RECEIVER = 'sample@pyar.org.ar'
TEST_SUBJECT = 'test subject'
TEST_BODY = 'test body'


def test_send_mail_to_publishers_with_mails():
    """
    Test send_mail_to_publishers sends mails when there are users with emails
    """
    joboffer = MagicMock()
    joboffer.get_publisher_mail_addresses = MagicMock(return_value=[TEST_RECEIVER])

    send_mail_to_publishers(joboffer, TEST_SUBJECT, TEST_BODY)

    assert len(mail.outbox) == 1

    assert mail.outbox[0].to == [TEST_RECEIVER]
    assert mail.outbox[0].subject == TEST_SUBJECT
    assert mail.outbox[0].body == TEST_BODY


def test_send_mail_to_publishers_without_emails():
    """
    Test send_mail_to_publishers doesn't send emails when there are no recipients
    """
    joboffer = MagicMock()
    joboffer.get_publisher_mail_addresses = MagicMock(return_value=[])

    send_mail_to_publishers(joboffer, TEST_SUBJECT, TEST_BODY)

    assert len(mail.outbox) == 0
