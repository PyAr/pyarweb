import factory
import pytest

from django.test import Client
from django.urls import reverse_lazy

from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD

from .factories import JobOfferFactory
from ..models import JobOffer


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


ADD_URL = reverse_lazy('joboffers:add')
ADMIN_URL = reverse_lazy('joboffers:admin')


@pytest.mark.django_db
def test_joboffer_creation_redirects_unlogged(client):
    response = client.get(ADD_URL)

    assert 302 == response.status_code
    assert f'/accounts/login/?next={ADD_URL}' == response.url


@pytest.mark.django_db
def test_joboffer_creation_with_all_fields_ok(logged_client):
    client = logged_client

    job_data = factory.build(dict, FACTORY_CLASS=JobOfferFactory)

    assert 0 == JobOffer.objects.count()

    response = client.post(ADD_URL, job_data)

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert 1 == JobOffer.objects.count()
    # TODO: Test for deactivated state
