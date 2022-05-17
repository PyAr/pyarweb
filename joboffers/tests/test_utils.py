import pytest

from smtplib import SMTPException
from unittest.mock import MagicMock, patch


from datetime import timedelta

from django.core import mail
from django.utils import timezone

from pycompanies.tests.factories import UserCompanyProfileFactory

from ..constants import EXPIRED_OFFER_MAIL_SUBJECT
from ..models import JobOffer, OfferState
from ..utils import (
  expire_old_offers,
  get_visualization_data,
  hash_secret, normalize_tags,
  send_mail_to_publishers
)
from .factories import JobOfferAccessLogFactory, JobOfferFactory


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
    repeated_tags = [
        'DñàÈ',
    ]
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


EXPECTED_SMTP_ERROR = 'random error'


@patch('joboffers.utils.send_mail', side_effect=SMTPException(EXPECTED_SMTP_ERROR))
def test_send_mail_logs_when_there_is_an_error(send_mail_function, caplog):
    """
    Test send_mail_to_publishers doesn't send emails when there is an error with the connection
    """
    joboffer = MagicMock()
    joboffer.get_publisher_mail_addresses = MagicMock(return_value=[TEST_RECEIVER])

    send_mail_to_publishers(joboffer, TEST_SUBJECT, TEST_BODY)
    assert len(mail.outbox) == 0
    assert caplog.messages[0] == EXPECTED_SMTP_ERROR


@pytest.mark.django_db
def test_get_visualization_data():
    """
    Test that get visualization works ok with a joboffer with visualizations
    """
    joboffer = JobOfferFactory.create()

    visualizations = JobOfferAccessLogFactory.create_batch(size=4, joboffer=joboffer)

    expected_data = [
      (
        visualization.created_at, visualization.joboffer.id, visualization.joboffer.title,
        visualization.event_type, visualization.get_event_type_display()
      )
      for visualization in visualizations
    ]

    data = get_visualization_data(joboffer)

    assert data == expected_data


@pytest.mark.django_db
def test_expire_old_offers():
    """
    Test expiration of old joboffers command
    """
    profile = UserCompanyProfileFactory.create()
    company = profile.company

    today = timezone.now()
    two_hundred_days_ago = today - timedelta(days=200)
    JobOfferFactory.create(company=company)
    offer2 = JobOfferFactory.create(company=company, state=OfferState.ACTIVE)
    offer3 = JobOfferFactory.create(company=company, state=OfferState.ACTIVE)
    JobOfferFactory.create(company=company, state=OfferState.ACTIVE)

    JobOffer.objects.filter(id__in=[offer2.id, offer3.id]).update(modified_at=two_hundred_days_ago)

    expire_old_offers()

    assert len(mail.outbox) == 2
    offers = JobOffer.objects.filter(state=OfferState.EXPIRED)
    assert mail.outbox[0].subject == EXPIRED_OFFER_MAIL_SUBJECT.format(title=offers[0].title)
    assert mail.outbox[1].subject == EXPIRED_OFFER_MAIL_SUBJECT.format(title=offers[1].title)
    assert JobOffer.objects.filter(state=OfferState.EXPIRED).count() == 2
