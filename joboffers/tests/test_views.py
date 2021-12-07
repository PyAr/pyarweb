import factory
import pytest

from django.contrib.messages import get_messages as contrib_get_messages
from django.test import Client
from django.urls import reverse, reverse_lazy

from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD

from .factories import JobOfferFactory
from ..models import JobOffer, OfferState


ADD_URL = 'joboffers:add'
ADMIN_URL = 'joboffers:admin'
APPROVE_URL = 'joboffers:approve'
REQUEST_MODERATION_URL = 'joboffers:request_moderation'


def get_plain_messages(request):
    """
    Gets a plain text message from a given request/response object. Useful for testing messages
    """
    messages = contrib_get_messages(request.wsgi_request)
    return [m.message for m in messages]


@pytest.fixture(name='client')
def create_client():
    return Client()


@pytest.fixture(name='user')
def create_user():
    return UserFactory()


@pytest.fixture(name='logged_client')
def create_logged_client(user):
    client = Client()
    client.login(username=user.username, password=DEFAULT_USER_PASSWORD)
    return client


@pytest.mark.django_db
def test_joboffer_creation_redirects_unlogged(client):
    target_url = reverse(ADD_URL)
    response = client.get(target_url)

    assert 302 == response.status_code
    assert f'/accounts/login/?next={target_url}' == response.url


@pytest.mark.django_db
def test_joboffer_creation_with_all_fields_ok(logged_client):
    client = logged_client
    target_url = reverse(ADD_URL)

    job_data = factory.build(dict, FACTORY_CLASS=JobOfferFactory)

    assert 0 == JobOffer.objects.count()

    response = client.post(target_url, job_data)

    assert 1 == JobOffer.objects.count()

    joboffer = JobOffer.objects.first()

    # Asserts redirection to the joboffer status page
    assert 302 == response.status_code
    assert f"/trabajo-nueva/{joboffer.slug}/" == response.url

    # Deactivated should be the first state
    assert OfferState.DEACTIVATED == joboffer.state

    obtained_messages = get_plain_messages(response)
    assert obtained_messages[0].startswith('Oferta creada correctamente.')


@pytest.mark.django_db
def test_joboffer_request_moderation_ok(logged_client):
    client = logged_client
    joboffer = JobOfferFactory.create()

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


@pytest.mark.django_db
def test_joboffer_approve_ok(logged_client):
    # TODO: Use a moderator user as logged user
    client = logged_client
    joboffer = JobOfferFactory.create(state=OfferState.MODERATION)

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
