import pytest

from django.db.utils import IntegrityError
from django.utils.text import slugify
from factory import Faker

from joboffers.models import Remoteness

from ..models import JobOffer
from .factories import JobOfferFactory
from .joboffers_descriptions import (LONG_JOBOFFER_DESCRIPTION, SHORT_JOBOFFER_DESCRIPTION,
                                     STRIPPED_SHORT_JOBOFFER_DESCRIPTION,
                                     STRIPPED_LONG_JOBOFFER_DESCRIPTION)


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
def test_assert_slug_is_updated_on_title_change():
    """
    Assert that a joboffer updates the slug after title update.
    """
    UPDATED_TITLE = 'Job Offer Updated'

    joboffer = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        title='Job Offer',
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None
    )

    joboffer.title = UPDATED_TITLE
    joboffer.save()

    assert slugify(UPDATED_TITLE) == joboffer.slug


@pytest.mark.django_db
def test_assert_short_description_is_set_with_stripped_description():
    """
    Assert that a joboffer short description is created with the stripped description
    if there is no short description given.
    """
    description = SHORT_JOBOFFER_DESCRIPTION
    short_description = STRIPPED_SHORT_JOBOFFER_DESCRIPTION

    joboffer = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        title='Job Offer',
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None,
        description=description,
        short_description='',
    )

    assert short_description == joboffer.short_description


@pytest.mark.django_db
def test_assert_short_description_is_set_with_the_given_short_description():
    """
    Assert that the joboffer doesn't update the short_description if it is provided in the model.
    """
    description = SHORT_JOBOFFER_DESCRIPTION

    SHORT_DESCRIPTION = 'short description'

    joboffer = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        title='Job Offer',
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None,
        description=description,
        short_description=SHORT_DESCRIPTION,
    )

    assert SHORT_DESCRIPTION == joboffer.short_description


@pytest.mark.django_db
def test_assert_get_short_description_strip_the_description():
    """
    Assert that get_short_description method strip the description correctly.
    """
    description = SHORT_JOBOFFER_DESCRIPTION
    short_description = STRIPPED_SHORT_JOBOFFER_DESCRIPTION

    assert short_description == JobOffer.get_short_description(description)


@pytest.mark.django_db
def test_assert_get_short_description_strip_the_long_description():
    """
    Assert that get_short_description method strip the description and limit to 512 chars.
    """
    description = LONG_JOBOFFER_DESCRIPTION
    short_description = STRIPPED_LONG_JOBOFFER_DESCRIPTION

    joboffer_short_description = JobOffer.get_short_description(description)

    assert 512 == len(joboffer_short_description)
    assert short_description == joboffer_short_description
