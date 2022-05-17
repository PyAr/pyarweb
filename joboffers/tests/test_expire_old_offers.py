import pytest

from datetime import timedelta

from django.core import mail
from django.utils import timezone

from pycompanies.tests.factories import UserCompanyProfileFactory

from .factories import JobOfferFactory
from ..constants import EXPIRED_OFFER_MAIL_SUBJECT
from ..models import JobOffer, OfferState
from ..management.commands.expire_old_offers import expire_old_offers


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
    JobOfferFactory.create(company=company, state=OfferState.ACTIVE)
    JobOfferFactory.create(company=company, state=OfferState.ACTIVE)

    JobOffer.objects.filter(id=offer2.id).update(modified_at=two_hundred_days_ago)

    expire_old_offers()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == EXPIRED_OFFER_MAIL_SUBJECT.format(title=offer2.title)
    assert JobOffer.objects.filter(state=OfferState.EXPIRED).count() == 1
