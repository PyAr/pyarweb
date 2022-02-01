import pytest
import factory

from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError

from easyaudit.models import CRUDEvent
from factory import Faker

from joboffers.models import Remoteness, OfferState
from pycompanies.tests.fixtures import create_user_company_profile # noqa

from .factories import JobOfferFactory, JobOfferCommentFactory
from ..models import JobOffer, JobOfferHistory


@pytest.mark.django_db
def test_assert_joboffer_when_remoteness_is_remote_location_can_be_null():
    """
    Assert that a joboffer can be created with a null location when remoteness is Remote.
    """
    JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        location=None,
        contact_mail=Faker('email')
    )

    assert JobOffer.objects.all().count() == 1


@pytest.mark.django_db
def test_assert_joboffer_when_remoteness_is_office_location_cannot_be_null():
    """
    Assert that a joboffer cannot be created with a null location when remoteness is in office.
    """
    with pytest.raises(IntegrityError):
        JobOfferFactory.create(
            remoteness=Remoteness.OFFICE,
            location=None,
            contact_mail=Faker('email')
        )


@pytest.mark.django_db
def test_assert_joboffer_when_remoteness_is_hybrid_location_cannot_be_null():
    """
    Assert the activation of a constraint when no location provided and the location is in office.
    """
    with pytest.raises(IntegrityError):
        JobOfferFactory.create(
            remoteness=Remoteness.HYBRID,
            location=None,
            contact_mail=Faker('email')
        )


@pytest.mark.django_db
def test_assert_constraint_contact_info_not_null():
    """
    Check constraint that assures that at least mail phone or url contact info is present.
    """
    with pytest.raises(IntegrityError):
        JobOfferFactory.create(
            remoteness=Remoteness.REMOTE,
            location=None,
            contact_mail=None,
            contact_phone=None,
            contact_url=None,
        )


@pytest.mark.django_db
def test_assert_joboffer_ok_when_just_one_contact_info_is_present():
    """
    Assert that a joboffer can be created with just one contact info.
    """
    joboffer_1 = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None
    )

    company = joboffer_1.company

    JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        company=company,
        location=None,
        contact_mail=None,
        contact_phone=Faker('pyint', min_value=11111111111, max_value=99999999999),
        contact_url=None
    )

    JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        company=company,
        location=None,
        contact_mail=None,
        contact_phone=None,
        contact_url=Faker('url')
    )

    assert JobOffer.objects.all().count() == 3


@pytest.mark.django_db
def test_get_joboffer_history_for_given_joboffer(user_company_profile, settings):
    """
    Test that the manager retrieves only the changes of the specified jobofffer
    """

    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    data = factory.build(
        dict,
        company=user_company_profile.company,
        created_by=user_company_profile.user,
        modified_by=user_company_profile.user,
        FACTORY_CLASS=JobOfferFactory
    )

    joboffer = JobOffer(**data)
    joboffer.save()
    joboffer.state = OfferState.MODERATION
    joboffer.save()

    comment = JobOfferCommentFactory.create(
        joboffer=joboffer, created_by=user_company_profile.user
    )
    JobOfferCommentFactory(created_by=user_company_profile.user)

    changes = JobOfferHistory.objects.for_offer(joboffer)

    actual_history = list(changes.values('event_type', 'content_type', 'object_id'))

    offer_ctype = ContentType.objects.get(app_label='joboffers', model='joboffer')
    offer_comment_ctype = ContentType.objects.get(
         app_label='joboffers', model='joboffercomment'
    )

    expected_history = [
        {
            'event_type': CRUDEvent.CREATE,
            'content_type': offer_comment_ctype.id,
            'object_id': str(comment.id)
        },
        {
            'event_type': CRUDEvent.UPDATE,
            'content_type': offer_ctype.id,
            'object_id': str(joboffer.id)
        },
        {
            'event_type': CRUDEvent.CREATE,
            'content_type': offer_ctype.id,
            'object_id': str(joboffer.id)
        }
    ]

    assert actual_history == expected_history
