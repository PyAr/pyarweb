import factory
import pytest

from datetime import datetime
from unittest.mock import patch

from django.core import mail
from django.urls import reverse

from pycompanies.tests.factories import UserCompanyProfileFactory
from pycompanies.tests.fixtures import create_user_company_profile # noqa
from pyarweb.tests.fixtures import create_user, create_logged_client # noqa

from ..constants import (
  ANALYTICS_URL,
  ANALYTICS_CSV_URL,
  ADD_URL,
  ADMIN_URL,
  APPROVE_URL,
  APPROVED_MAIL_SUBJECT,
  DEACTIVATE_URL,
  HISTORY_URL,
  LIST_URL,
  PUBLISHER_FAILED_ERROR,
  REACTIVATE_URL,
  REACTIVATED_MAIL_SUBJECT,
  REJECT_URL,
  REJECTED_MAIL_SUBJECT,
  REQUEST_MODERATION_URL,
  TRACK_CONTACT_INFO_URL,
  TELEGRAM_APPROVED_MESSAGE,
  TELEGRAM_MODERATION_MESSAGE,
  TELEGRAM_REJECT_MESSAGE,
  VIEW_URL
)
from ..models import EventType, JobOffer, JobOfferHistory, JobOfferAccessLog, OfferState
from ..publishers import Publisher
from ..views import STATE_LABEL_CLASSES
from .factories import JobOfferCommentFactory, JobOfferFactory, JobOfferAccessLogFactory
from .fixtures import create_admin_user, create_publisher_client, create_telegram_dummy # noqa
from .utils import get_plain_messages, create_analytics_sample_data

JOBOFFER_TITLE1 = 'Job Offer Sample Title 1'
JOBOFFER_TITLE2 = 'Job Offer Sample Title 2'
JOBOFFER_TITLE3 = 'Job Offer Sample Title 3'
JOBOFFER_TITLE4 = 'Job Offer Sample Title 4'
JOBOFFER_TITLE5 = 'Job Offer Sample Title 5'

JOBOFFER_TAG_1 = 'tag1'
JOBOFFER_TAG_2 = 'tag2'
JOBOFFER_TAG_3 = 'tag3'
JOBOFFER_TAG_4 = 'tag4'
JOBOFFER_TAG_5 = 'tag5'


@pytest.mark.django_db
def test_joboffer_creation_redirects_unlogged(client):
    target_url = reverse(ADD_URL)
    response = client.get(target_url)

    assert 302 == response.status_code
    assert f'/accounts/login/?next={target_url}' == response.url


@pytest.mark.django_db
def test_joboffer_create_form_render_should_redirect_for_an_user_without_company(
        logged_client
):
    """
    Test that the get request to the joboffer's create view redirects for an user without company
    """

    client = logged_client
    target_url = reverse(ADD_URL)

    response = client.get(target_url)
    message = ("No estas relacionade a ninguna empresa. Asociate a una para poder "
               "crear una oferta de trabajo.")

    assert message == get_plain_messages(response)[0]
    assert response.status_code == 302


@pytest.mark.django_db
def test_joboffer_admin_should_redirect_for_an_user_without_company(
        logged_client
):
    """
    Test that the get request to the joboffer's admin view redirects for an user without company
    """

    client = logged_client
    target_url = reverse(ADMIN_URL)

    response = client.get(target_url)
    message = ("No estas relacionade a ninguna empresa. Asociate a una para poder "
               "crear una oferta de trabajo.")

    assert message == get_plain_messages(response)[0]
    assert response.status_code == 302


@pytest.mark.django_db
def test_joboffer_create_form_render_should_not_redirect_for_an_user_with_company(
        logged_client, user
):
    """
    Test that the get request to the joboffer's create view doesn't redirect for
    an user with company
    """

    client = logged_client
    target_url = reverse(ADD_URL)

    UserCompanyProfileFactory.create(user=user)

    response = client.get(target_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_creation_should_fail_for_an_user_from_a_different_company(
        logged_client, user_company_profile
):
    """
    Test that the post request to the joboffer's create view fails for not allowed user
    """
    client = logged_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    assert JobOffer.objects.count() == 0

    response = client.post(target_url, job_data)

    assert response.status_code == 403
    assert JobOffer.objects.count() == 0


@pytest.mark.django_db
def test_joboffer_creation_as_admin_should_fail(admin_client, user_company_profile):
    """
    Test joboffer creation is not allowed as admin user
    """
    client = admin_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company

    job_data = factory.build(dict, company=company.id, FACTORY_CLASS=JobOfferFactory)

    del job_data['company']

    assert 0 == JobOffer.objects.count()

    response = client.post(target_url, job_data)

    assert JobOffer.objects.count() == 0
    # Asserts redirection to the joboffer status page
    assert response.status_code == 403


@pytest.mark.django_db
def test_joboffer_request_moderation_ok(publisher_client, user_company_profile, telegram_dummy):
    """
    Test request for moderation for a publisher user
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company)

    target_url = reverse(REQUEST_MODERATION_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.DEACTIVATED == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta enviada a moderación")

    joboffer = JobOffer.objects.first()
    assert OfferState.MODERATION == joboffer.state

    telegram_history = telegram_dummy.call_history
    assert len(telegram_history) == 1
    sent_message = telegram_history[0]['text'][0]
    assert sent_message.endswith(TELEGRAM_MODERATION_MESSAGE.format(
      offer_url=joboffer.get_full_url()
    ))


@pytest.mark.django_db
def test_joboffer_deactivate_ok(publisher_client, user_company_profile):
    """
    Test deactivate a joboffer by a publisher
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company, state=OfferState.ACTIVE)

    target_url = reverse(DEACTIVATE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert joboffer.state == OfferState.ACTIVE
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta desactiva")

    joboffer = JobOffer.objects.get(id=joboffer.id)
    assert OfferState.DEACTIVATED == joboffer.state


@pytest.mark.django_db
def test_joboffer_reactivate_ok(publisher_client, user_company_profile):
    """
    Test reactiving a joboffer by a publisher
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company, state=OfferState.EXPIRED)

    target_url = reverse(REACTIVATE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert joboffer.state == OfferState.EXPIRED
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta reactivada")

    joboffer = JobOffer.objects.get(id=joboffer.id)
    assert OfferState.ACTIVE == joboffer.state

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user_company_profile.user.email]
    assert mail.outbox[0].subject == REACTIVATED_MAIL_SUBJECT


@pytest.fixture(name="joboffers_list")
def create_joboffers_list(user_company_profile):
    company = user_company_profile.company

    JobOfferFactory.create(  # Job offer from a different company
        title=JOBOFFER_TITLE5,
        tags=[JOBOFFER_TAG_5]
    )

    return [
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE1,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 20),
            state=OfferState.ACTIVE
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE2,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 21),
            state=OfferState.ACTIVE
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE3,
            tags=[JOBOFFER_TAG_2],
            created_at=datetime(2021, 12, 22),
            state=OfferState.ACTIVE
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE4,
            tags=[JOBOFFER_TAG_4],
            created_at=datetime(2021, 12, 22),
            state=OfferState.ACTIVE
        )
    ]


@pytest.mark.django_db
def test_joboffer_admin_works_with_random_query_search(publisher_client, joboffers_list):
    """
    Test that an empty queryset is returned for random search
    """
    client = publisher_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': 'thing Ç '})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    assert list(actual_joboffers) == []


@pytest.mark.django_db
def test_joboffer_admin_works_with_empty_query_search(publisher_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = publisher_client

    target_url = reverse('joboffers:admin')
    response = client.get(target_url, {'q': ''})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_admin_works_without_query(publisher_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = publisher_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url)

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_approve_without_permission(publisher_client, user_company_profile):
    """
    Test approval of a joboffer with a publisher should fail and keep the same state in the offer
    """
    client = publisher_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company, state=OfferState.MODERATION)

    target_url = reverse(APPROVE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 403 == response.status_code
    joboffer = JobOffer.objects.first()
    assert joboffer.state == OfferState.MODERATION


@pytest.mark.django_db
@patch('joboffers.views.publish_to_all_social_networks')
def test_joboffer_approve_ok(
    publish_function, admin_client, admin_user, user_company_profile, telegram_dummy
):
    """
    Test approval of a joboffer with an admin user
    """
    client = admin_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION, company=company)

    target_url = reverse(APPROVE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions

    response = client.get(target_url)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta aceptada y activada.")

    joboffer = JobOffer.objects.first()
    assert OfferState.ACTIVE == joboffer.state

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user_company_profile.user.email]
    assert mail.outbox[0].subject == APPROVED_MAIL_SUBJECT

    telegram_history = telegram_dummy.call_history
    assert len(telegram_history) == 1
    sent_message = telegram_history[0]['text'][0]
    assert sent_message.endswith(TELEGRAM_APPROVED_MESSAGE.format(
      offer_url=joboffer.get_full_url(),
      username=admin_user.username
    ))

    assert publish_function.called
    assert publish_function.call_args[0][0] == joboffer


class FailingPublisher(Publisher):
    name = "Dummy"

    def publish(self, jobo_ffer):
        """Fails to publish for testing purposes"""
        return self.RESULT_BAD


@pytest.mark.django_db
def test_joboffer_approve_failed_to_publish(
    admin_client, admin_user, user_company_profile, telegram_dummy, settings
):
    """Test that approving a joboffer with a failing publisher adds an error message"""
    client = admin_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION, company=company)

    target_url = reverse(APPROVE_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions

    settings.SOCIAL_NETWORKS_PUBLISHERS = ['joboffers.tests.test_views.FailingPublisher']

    response = client.get(target_url)

    messages = get_plain_messages(response)
    expected_message = PUBLISHER_FAILED_ERROR.format(publisher=FailingPublisher.name)
    assert expected_message in messages


@pytest.mark.django_db
def test_joboffer_reject_ok(admin_client, admin_user, user_company_profile, telegram_dummy):
    """
    Test rejection of the joboffer by the admin user
    """

    client = admin_client
    company = user_company_profile.company
    joboffer = JobOfferFactory.create(company=company, state=OfferState.MODERATION)

    target_url = reverse(REJECT_URL, kwargs={'slug': joboffer.slug})

    assert 1 == JobOffer.objects.count()
    assert OfferState.MODERATION == joboffer.state
    # end preconditions check

    comment_data = factory.build(dict, joboffer=joboffer.id, FACTORY_CLASS=JobOfferCommentFactory)

    response = client.post(target_url, data=comment_data)

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    messages = get_plain_messages(response)
    assert messages[0].startswith("Oferta rechazada.")

    joboffer = JobOffer.objects.first()
    assert joboffer.state == OfferState.REJECTED

    assert len(mail.outbox) == 1
    assert REJECTED_MAIL_SUBJECT

    telegram_history = telegram_dummy.call_history
    assert len(telegram_history) == 1
    sent_message = telegram_history[0]['text'][0]
    assert sent_message.endswith(TELEGRAM_REJECT_MESSAGE.format(
      offer_title=joboffer.title,
      offer_url=joboffer.get_full_url(),
      username=admin_user.username
    ))


@pytest.mark.django_db
def test_joboffer_form_with_initial_user_company(user, publisher_client, user_company_profile):
    """
    Assert that the form inits with the associated user company
    """
    client = publisher_client
    target_url = reverse(ADD_URL)
    company = user_company_profile.company
    factory.build(dict, user=user.id, company=company.id, FACTORY_CLASS=JobOfferFactory)

    response = client.get(target_url)

    assert company == response.context['form'].initial['company']


@pytest.mark.django_db
def test_joboffer_view_as_anonymous(client):
    """
    Test that the joboffer detail view renders without error as anonymous user
    """
    joboffer = JobOfferFactory.create()

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 200
    assert response.context_data['action_buttons'] == []


@pytest.mark.django_db
def test_joboffer_create_view_as_publisher(publisher_client):
    """
    Test that the joboffer detail view renders without error as a publisher
    """
    client = publisher_client

    target_url = reverse(ADD_URL)

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_admin_filters_by_joboffer_title(publisher_client, joboffers_list):
    """
    Test that searching by title2 retrieves only title2 joboffer
    """
    client = publisher_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': JOBOFFER_TITLE2})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2]


@pytest.mark.django_db
def test_joboffer_admin_filters_by_exactly_by_tagname(publisher_client, joboffers_list):
    """
    Test that searching by tag retrieves only the offers that match exactly with the tag name
    """
    client = publisher_client

    target_url = reverse('joboffers:admin')

    response = client.get(target_url, {'q': 'tag1'})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2, JOBOFFER_TITLE1]


@pytest.mark.django_db
def test_joboffer_create_view_as_publusher(publisher_client):
    """
    Test that the joboffer create view renders without error as anonymous user
    """
    client = publisher_client

    target_url = reverse(ADD_URL)

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_active_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with active label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.ACTIVE)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    label_class = STATE_LABEL_CLASSES[OfferState.ACTIVE]

    assert response.context_data['state_label_class'] == label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_deactivated_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with deactivated label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.DEACTIVATED]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_expired_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with expired label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.EXPIRED)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.EXPIRED]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_moderation_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with moderation label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.MODERATION]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_new_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with new label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.NEW)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.NEW]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_joboffer_detail_view_render_state_with_rejected_label(publisher_client):
    """
    Test that the joboffer detail view renders the state with rejected label class
    """
    client = publisher_client
    joboffer = JobOfferFactory.create(state=OfferState.REJECTED)
    JobOfferCommentFactory.create(joboffer=joboffer)

    target_url = reverse(VIEW_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    state_label_class = STATE_LABEL_CLASSES[OfferState.REJECTED]

    assert response.context_data['state_label_class'] == state_label_class


@pytest.mark.django_db
def test_JobOfferHistoryView_renders_with_context(
        publisher_client, settings, user_company_profile, admin_user
):
    """
    Test that JobOfferHistoryView renders correctly
    """
    settings.TEST = True
    # ^ This is needed so django-easyaudit creates the CRUDEvent objects in the
    # same trasnaction and then we can test for it.

    client = publisher_client
    user = user_company_profile.user
    company = user_company_profile.company

    joboffer = JobOfferFactory.build(company=company, created_by=user, modified_by=user)
    joboffer.save()
    joboffer.state = OfferState.MODERATION
    joboffer.save()
    comment = JobOfferCommentFactory.build(joboffer=joboffer, created_by=admin_user)
    comment.save()
    joboffer.state = OfferState.ACTIVE
    joboffer.save()

    target_url = reverse(HISTORY_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    object_list = response.context_data['object_list'].values('event_type', 'content_type__model')
    object_list = list(object_list)

    assert object_list == [
        {'event_type': JobOfferHistory.UPDATE, 'content_type__model': 'joboffer'},
        {'event_type': JobOfferHistory.CREATE, 'content_type__model': 'joboffercomment'},
        {'event_type': JobOfferHistory.UPDATE, 'content_type__model': 'joboffer'},
        {'event_type': JobOfferHistory.CREATE, 'content_type__model': 'joboffer'}
    ]


@pytest.mark.django_db
def test_joboffer_list_view_includes_user_and_own_company_for_publisher(publisher_client):
    """
    Test that the joboffer list view includes user and own_company in the companies for a publisher
    """
    client = publisher_client
    JobOfferFactory.create(state=OfferState.ACTIVE)

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert response.context_data['user'].is_authenticated
    assert response.context_data['own_company']


@pytest.mark.django_db
def test_joboffer_list_view_includes_user_and_own_company_for_user_without_company(logged_client):
    """
    Test that the joboffer list view includes user and own_company in the companies for user
    without company
    """
    client = logged_client
    JobOfferFactory.create(state=OfferState.ACTIVE)

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert response.context_data['user'].is_authenticated
    assert 'own_company' not in response.context_data


@pytest.mark.django_db
def test_joboffer_list_view_includes_user_and_own_company_for_unlogged_user(client):
    """
    Test that the joboffer list view includes user and own_company for anonymous user
    """
    JobOfferFactory.create(state=OfferState.ACTIVE)

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert response.context_data['user'].is_anonymous
    assert 'own_company' not in response.context_data


@pytest.mark.django_db
def test_joboffer_list_view_render_list_with_an_active_joboffer(publisher_client):
    """
    Test that the joboffer list view renders the list with an active joboffer
    """
    client = publisher_client
    JobOfferFactory.create(state=OfferState.ACTIVE)
    JobOfferFactory.create(state=OfferState.EXPIRED, title="Second Joboffer")

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert len(response.context_data['object_list']) == 1


@pytest.mark.django_db
def test_joboffer_list_view_render_empty_list(publisher_client):
    """
    Test that the joboffer list view renders an empty list if there is no joboffers
    """
    client = publisher_client

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert len(response.context_data['object_list']) == 0


@pytest.mark.django_db
def test_joboffer_list_view_render_empty_if_no_active_joboffers(publisher_client):
    """
    Test that the joboffer list view renders an empty list if there is no active joboffer
    """
    client = publisher_client
    JobOfferFactory.create(state=OfferState.NEW, title="First Joboffer")
    JobOfferFactory.create(state=OfferState.EXPIRED, title="Second Joboffer")

    target_url = reverse(LIST_URL)

    response = client.get(target_url)

    assert len(response.context_data['object_list']) == 0


@pytest.mark.django_db
def test_joboffer_list_view_render_with_an_active_and_expired_joboffer(publisher_client):
    """
    Test that the joboffer list view renders the list with active and expired joboffers if
    the active checkbox is not checked.
    """
    client = publisher_client
    JobOfferFactory.create(state=OfferState.ACTIVE, title="First Joboffer")
    JobOfferFactory.create(state=OfferState.EXPIRED, title="Second Joboffer")
    JobOfferFactory.create(state=OfferState.NEW, title="Third Joboffer")

    target_url = reverse(LIST_URL)

    response = client.get(target_url, {'active': 'false'})

    assert len(response.context_data['object_list']) == 2


@pytest.mark.django_db
def test_joboffer_list_view_render_with_the_joboffer_that_matches_the_search(publisher_client):
    """
    Test that the joboffer list view renders the joboffers that matches the title content with
    the given search.
    """
    client = publisher_client
    JobOfferFactory.create(state=OfferState.ACTIVE, title="First Joboffer")
    second_joboffer = JobOfferFactory.create(state=OfferState.ACTIVE, title="Second Joboffer")

    target_url = reverse(LIST_URL)

    response = client.get(target_url, {'search': 'second'})

    assert response.context_data['object_list'][0] == second_joboffer


@pytest.mark.django_db
def test_joboffer_list_view_render_with_joboffer_that_matches_the_description(publisher_client):
    """
    Test that the joboffer list view renders the joboffers that matches the title content with
    the given search.
    """
    client = publisher_client
    first_joboffer = JobOfferFactory.create(state=OfferState.ACTIVE, description="First Joboffer")
    JobOfferFactory.create(state=OfferState.ACTIVE, description="Second Joboffer")

    target_url = reverse(LIST_URL)

    response = client.get(target_url, {'search': 'first'})

    assert response.context_data['object_list'][0] == first_joboffer


@pytest.mark.django_db
def test_joboffer_list_view_render_the_joboffer_that_contains_the_given_tag(client):
    """
    Test that the joboffer list view renders the joboffer that contains the given tag, with
    a unlogged user.
    """
    first_joboffer = JobOfferFactory.create(
        state=OfferState.ACTIVE,
        description='First Joboffer',
        tags=['django']
    )

    JobOfferFactory.create(
        state=OfferState.ACTIVE,
        description='Second Joboffer',
        tags=['javascript']
    )

    target_url = reverse(LIST_URL)

    response = client.get(target_url, {'tag_django': '1'})

    assert len(response.context_data['object_list']) == 1
    assert response.context_data['object_list'][0] == first_joboffer


@pytest.mark.django_db
def test_joboffer_list_view_count(client, joboffers_list):
    """
    Test that accessing the joboffer's list page only gives one view
    """
    target_url = reverse(LIST_URL)

    response1 = client.get(target_url)
    response2 = client.get(target_url)

    assert response1.status_code == 200
    assert response2.status_code == 200

    views_counted = JobOfferAccessLog.objects.filter(event_type=EventType.LISTING_VIEW).count()

    assert views_counted == len(joboffers_list)


@pytest.mark.django_db
def test_joboffer_list_first_page_view_count(client):
    """
    Test that accessing the joboffer's list page only counts the first 20 joboffers
    """
    target_url = reverse(LIST_URL)

    JobOfferFactory.create_batch(size=30, state=OfferState.ACTIVE)

    response1 = client.get(target_url)
    response2 = client.get(target_url)

    assert response1.status_code == 200
    assert response2.status_code == 200

    views_counted = JobOfferAccessLog.objects.filter(event_type=EventType.LISTING_VIEW).count()

    assert views_counted == 20


@pytest.mark.django_db
def test_joboffer_individual_view_count(client, joboffers_list):
    """
    Test that accessing the joboffer's detail page only gives one view
    """
    target_url = reverse(VIEW_URL, kwargs={'slug': joboffers_list[0].slug})

    response1 = client.get(target_url)
    response2 = client.get(target_url)
    assert response1.status_code == 200
    assert response2.status_code == 200

    assert JobOfferAccessLog.objects.filter(event_type=EventType.DETAIL_VIEW).count() == 1


@pytest.mark.django_db
def test_joboffer_individual_contact_info_view_count(client, joboffers_list):
    """
    Test that accessing the joboffer's detail page only gives one view
    """
    target_url = reverse(TRACK_CONTACT_INFO_URL, kwargs={'slug': joboffers_list[0].slug})

    response1 = client.post(target_url)
    response2 = client.post(target_url)
    assert response1.status_code == 204
    assert response2.status_code == 204

    views_counted = JobOfferAccessLog.objects.filter(
        event_type=EventType.CONTACT_INFO_VIEW).count()

    assert views_counted == 1


@pytest.mark.django_db
def test_JobOfferAnalyticsView_get_is_forbidden_for_non_publisher(logged_client):
    """
    Test that the JobOfferAnalyticsView views doesn't allow anonymous
    """
    client = logged_client
    joboffer = JobOfferFactory.create()

    target_url = reverse(ANALYTICS_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_JobOfferAnalyticsView_get_renders_ok_for_admin(admin_client):
    """
    Test that the JobOfferAnalyticsView views renders ok for admin users
    """
    client = admin_client
    joboffer = JobOfferFactory.create()

    target_url = reverse(ANALYTICS_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_JobOfferAnalyticsView_get_renders_ok_for_publisher(
    publisher_client, user_company_profile
):
    """
    Test that the JobOfferAnalyticsView views renders without errors for the publisher of the
    joboffer
    """
    client = publisher_client

    joboffer = JobOfferFactory.create(company=user_company_profile.company)
    JobOfferAccessLogFactory.create_batch(joboffer=joboffer, size=10)

    target_url = reverse(ANALYTICS_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 200


@pytest.mark.django_db
@patch('joboffers.views.get_visualizations_graph')
def test_render_joboffers_analytics_and_counts_ok(
    get_visualizations_graph_mock, publisher_client, user_company_profile
):
    """
    Test that the rendering of JobOfferAccessLog data for a joboffer doesn't fail and matches the
    expected visualizations amounts.
    """
    client = publisher_client
    company = user_company_profile.company
    user = user_company_profile.user

    joboffer, expected_total_job_views = create_analytics_sample_data(
      test_username=user.username,
      test_offer_title='Testing Offer 1',
      test_company=company,
      max_views_amount=10
    )

    target_url = reverse(ANALYTICS_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)
    assert response.status_code == 200

    assert get_visualizations_graph_mock.call_count == 3

    call_list = get_visualizations_graph_mock.call_args_list

    total_views = sum([sum(args[0][1]) for args in call_list])

    assert total_views == expected_total_job_views

    table_data = response.context['totals']

    table_views = sum([views for _, views in table_data])

    assert table_views == expected_total_job_views


@pytest.mark.django_db
def test_DownloadAnalitycAsCsv_returns_a_csv_for_publisher(publisher_client, user_company_profile):
    """
    Test that the DownloadAnalyticsAsCsv view returns a csv file for a publisher
    """
    client = publisher_client

    joboffer = JobOfferFactory.create(company=user_company_profile.company)
    JobOfferAccessLogFactory.create_batch(joboffer=joboffer, size=10)

    target_url = reverse(ANALYTICS_CSV_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv'


@pytest.mark.django_db
def test_DownloadAnalitycAsCsv_returns_forbidden_for_anonymous_user(client):
    """
    Test that the DownloadAnalyticsAsCsv view returns a csv file for a publisher
    """
    joboffer = JobOfferFactory.create()
    JobOfferAccessLogFactory.create_batch(joboffer=joboffer, size=10)

    target_url = reverse(ANALYTICS_CSV_URL, kwargs={'slug': joboffer.slug})

    response = client.get(target_url)

    assert response.status_code == 403
