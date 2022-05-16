import factory
import pytest

from datetime import date
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.backends.db import SessionStore
from django.db.utils import IntegrityError
from django.utils.text import slugify
from easyaudit.models import CRUDEvent
from factory import Faker

from pycompanies.tests.factories import UserCompanyProfileFactory
from pycompanies.tests.fixtures import create_user_company_profile  # noqa
from ..constants import STATE_LABEL_CLASSES
from ..models import (EventType, JobOffer, JobOfferHistory, JobOfferAccessLog, OfferState,
                      Remoteness)
from .factories import JobOfferAccessLogFactory, JobOfferCommentFactory, JobOfferFactory
from .joboffers_descriptions import (LONG_JOBOFFER_DESCRIPTION,
                                     SHORT_JOBOFFER_DESCRIPTION,
                                     STRIPPED_LONG_JOBOFFER_DESCRIPTION,
                                     STRIPPED_SHORT_JOBOFFER_DESCRIPTION)


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


@pytest.mark.django_db
def test_JobOfferHistory_joboffer_comment_with_wrong_model_object(settings):
    """
    Test that calling comment_fields on JobOfferHistory object raises exceptions when it is called
    with an object different that JobOfferComment
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    JobOfferFactory.create()

    history = JobOfferHistory.objects.first()

    assert history.content_type.model == 'joboffer'

    with pytest.raises(ValueError):
        history.joboffer_comment


@pytest.mark.django_db
def test_JobOfferHistory_works_with_a_JobOfferComment_model(settings):
    """
    Test that a JobOfferHistory returns the related JobOfferComment correctly
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    comment = JobOfferCommentFactory.create()

    history = JobOfferHistory.objects.first()

    assert history.content_type.model == 'joboffercomment'

    obtained_comment = history.joboffer_comment

    assert comment == obtained_comment


@pytest.mark.django_db
def test_JobOfferHistory_changes(settings):
    """
    Test that JobOfferHistory.fields returns the serialized fields for a joboffer
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)
    joboffer.state = OfferState.ACTIVE
    joboffer.save()

    history = JobOfferHistory.objects.filter(event_type=JobOfferHistory.UPDATE).first()

    assert history.content_type.model == 'joboffer'

    changes = history.changes

    assert changes['state'] == [OfferState.DEACTIVATED, OfferState.ACTIVE]


@pytest.mark.django_db
def test_JobOfferHistory_fields(settings):
    """
    Test that JobOfferHistory.fields returns the serialized fields for a joboffer
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    joboffer = JobOfferFactory.create()

    history = JobOfferHistory.objects.first()

    assert history.content_type.model == 'joboffer'

    fields = history.fields

    assert joboffer.title == fields['title']


@pytest.mark.django_db
def test_JobOfferHistory_state_label(settings):
    """
    Test that JobOfferHistory.state return a state correctly.
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    joboffer = JobOfferFactory.create()

    history = JobOfferHistory.objects.first()

    assert history.content_type.model == 'joboffer'

    state_label = history.state_label

    assert joboffer.state.label == state_label


@pytest.mark.django_db
def test_JobOfferHistory_state_label_class(settings):
    """
    Test that state_class return a class for a joboffer JobOfferHistory
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    JobOfferFactory.create(state=OfferState.MODERATION)

    history = JobOfferHistory.objects.first()

    assert history.content_type.model == 'joboffer'

    state_label_class = history.state_label_class

    assert state_label_class == STATE_LABEL_CLASSES[OfferState.MODERATION]


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

    joboffer = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        title='Job Offer',
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None,
        description=SHORT_JOBOFFER_DESCRIPTION,
        short_description='',
    )

    assert STRIPPED_SHORT_JOBOFFER_DESCRIPTION == joboffer.short_description


@pytest.mark.django_db
def test_assert_short_description_is_set_with_the_given_short_description():
    """
    Assert that the joboffer doesn't update the short_description if it is provided in the model.
    """
    short_description = 'short description'

    joboffer = JobOfferFactory.create(
        remoteness=Remoteness.REMOTE,
        title='Job Offer',
        location=None,
        contact_mail=Faker('email'),
        contact_phone=None,
        contact_url=None,
        description=SHORT_JOBOFFER_DESCRIPTION,
        short_description=short_description,
    )

    assert short_description == joboffer.short_description


@pytest.mark.django_db
def test_assert_get_short_description_strip_the_description():
    """
    Assert that get_short_description method strip the description correctly.
    """
    short_description = JobOffer.get_short_description(SHORT_JOBOFFER_DESCRIPTION)
    assert STRIPPED_SHORT_JOBOFFER_DESCRIPTION == short_description


@pytest.mark.django_db
def test_assert_get_short_description_strip_the_long_description():
    """
    Assert that get_short_description method strip the description and limit to 512 chars.
    """
    short_description = JobOffer.get_short_description(LONG_JOBOFFER_DESCRIPTION)

    assert 512 == len(short_description)
    assert STRIPPED_LONG_JOBOFFER_DESCRIPTION == short_description


@pytest.mark.django_db
def test_joboffer_last_comment():
    """
    Test the joboffer.last_comment property
    """
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)
    JobOfferCommentFactory.create(joboffer=joboffer)
    expected_comment = JobOfferCommentFactory.create(joboffer=joboffer)

    assert joboffer.last_comment.text == expected_comment.text


@pytest.mark.django_db
def test_joboffer_track_visualization_with_empty_session():
    """
    Test calling joboffer.track_visualization with an empty session
    """
    joboffer = JobOfferFactory.create()
    session = SessionStore()
    track_record, created = joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert created is True

    assert track_record.event_type == EventType.DETAIL_VIEW
    assert track_record.joboffer == joboffer
    assert JobOfferAccessLog.objects.count() == 1


@pytest.mark.django_db
def test_joboffer_track_visualization_with_initiated_session():
    """
    Test calling joboffer.track_visualization with initiated sesion
    """
    joboffer = JobOfferFactory.create()
    session = SessionStore()
    session.create()
    track_record, created = joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert created is True

    assert track_record.event_type == EventType.DETAIL_VIEW
    assert track_record.joboffer == joboffer
    assert JobOfferAccessLog.objects.count() == 1


@pytest.mark.django_db
def test_joboffer_track_visualization_should_not_repeat_multiple_hits():
    """
    Test calling joboffer.track_visualization multiple times with the same session doesn't count
    additional views
    """
    joboffer = JobOfferFactory.create()
    session = SessionStore()
    session.create()
    track_record, created = joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert created is True

    for i in range(10):
        joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert JobOfferAccessLog.objects.count() == 1


@pytest.mark.django_db
def test_joboffer_track_visualization_should_count_different_sessiones_on_the_same_day():
    """
    Test calling joboffer.track_visualization multiple times with different sessions counts ok
    """
    joboffer = JobOfferFactory.create()

    EXPECTED_VISUALIZATIONS = 10

    for i in range(EXPECTED_VISUALIZATIONS):
        session = SessionStore()
        session.create()
        joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert JobOfferAccessLog.objects.count() == EXPECTED_VISUALIZATIONS


@pytest.mark.django_db
def test_joboffer_track_visualization_should_count_different_sessiones_on_different_months():
    """
    Test that calling joboffer.track_visualization counts two hits from today and from a previous
    month (same session).
    """
    joboffer = JobOfferFactory.create()

    EXPECTED_VISUALIZATIONS = 2

    session = SessionStore()
    session.create()

    previous_date = date(2022, 2, 1)

    with patch('joboffers.models.date') as mocked_date:
        mocked_date.today.return_value = previous_date
        # Previous month's hit
        joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    # Today's hit
    joboffer.track_visualization(session, event_type=EventType.DETAIL_VIEW)

    assert JobOfferAccessLog.objects.count() == EXPECTED_VISUALIZATIONS


@pytest.mark.django_db
def test_joboffer_get_publisher_mail_addresses_with_multiple_users():
    profile1 = UserCompanyProfileFactory.create()
    company = profile1.company
    profile2 = UserCompanyProfileFactory.create(company=company)
    joboffer = JobOfferFactory.create(company=company)

    EXPECTED_MAILS = {profile1.user.email, profile2.user.email}

    mails = joboffer.get_publisher_mail_addresses()

    assert mails == EXPECTED_MAILS


@pytest.mark.django_db
def test_joboffer_get_publisher_mail_addresses_without_users():
    joboffer = JobOfferFactory.create()

    EXPECTED_MAILS = set()

    mails = joboffer.get_publisher_mail_addresses()

    assert mails == EXPECTED_MAILS


@pytest.mark.django_db
def test_joboffer_get_visualizations_full():
    """
    Test get_visualizations with all the event types
    """
    joboffer = JobOfferFactory.create()
    JobOfferAccessLogFactory.create_batch(
      size=1, event_type=EventType.LISTING_VIEW, joboffer=joboffer
    )
    JobOfferAccessLogFactory.create_batch(
      size=2, event_type=EventType.DETAIL_VIEW, joboffer=joboffer
    )
    JobOfferAccessLogFactory.create_batch(
      size=3, event_type=EventType.CONTACT_INFO_VIEW, joboffer=joboffer
    )

    visualizations = joboffer.get_visualizations_count()

    assert visualizations[EventType.LISTING_VIEW] == 1
    assert visualizations[EventType.DETAIL_VIEW] == 2
    assert visualizations[EventType.CONTACT_INFO_VIEW] == 3


@pytest.mark.django_db
def test_joboffer_get_visualizations_some():
    """
    Test get_visualizations with only listing view type
    """
    joboffer = JobOfferFactory.create()
    JobOfferAccessLogFactory.create_batch(
      size=1, event_type=EventType.LISTING_VIEW, joboffer=joboffer
    )

    visualizations = joboffer.get_visualizations_count()

    assert visualizations == {EventType.LISTING_VIEW: 1}


@pytest.mark.django_db
def test_joboffer_get_visualizations_empty():
    """
    Test get_visualizations without access log
    """
    joboffer = JobOfferFactory.create()

    visualizations = joboffer.get_visualizations_count()

    assert visualizations == {}
