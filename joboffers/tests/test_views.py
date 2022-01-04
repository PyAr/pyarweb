import factory
import pytest

from datetime import datetime
from django.test import Client
from django.urls import reverse_lazy

from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD
from pycompanies.tests.factories import UserCompanyProfileFactory
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


# TODO: Replace with the one in the pycompany app when get merged
@pytest.fixture(name='user_company_profile')
def create_user_company_profile():
    """
    Fixture with a dummy UserCompanyProfileFactory
    """
    return UserCompanyProfileFactory.create()


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

    del job_data['company']

    assert 0 == JobOffer.objects.count()

    response = client.post(ADD_URL, job_data)

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert 1 == JobOffer.objects.count()
    # TODO: Test for deactivated state


JOBOFFER_TITLE1 = 'title1'
JOBOFFER_TITLE2 = 'title2'
JOBOFFER_TITLE3 = 'title3'

JOBOFFER_TAG_1 = 'tag1'
JOBOFFER_TAG_2 = 'tag2'


@pytest.fixture(name="joboffers_list")
def create_joboffers_list(user_company_profile):
    company = user_company_profile.company

    return [
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE1,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 20)
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE2,
            tags=[JOBOFFER_TAG_1],
            created_at=datetime(2021, 12, 21)
        ),
        JobOfferFactory.create(
            company=company,
            title=JOBOFFER_TITLE3,
            tags=[JOBOFFER_TAG_2],
            created_at=datetime(2021, 12, 22)
        )
    ]


@pytest.mark.django_db
def test_joboffer_admin_works_with_random_query_search(logged_client, joboffers_list):
    """
    Test that an empty queryset
    """
    client = logged_client

    target_url = reverse_lazy('joboffers:admin')

    response = client.get(target_url, {'q': 'unexistant thing Ç '})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    assert list(actual_joboffers) == []


@pytest.mark.django_db
def test_joboffer_admin_works_with_empty_query_search(logged_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = logged_client

    target_url = reverse_lazy('joboffers:admin')

    response = client.get(target_url, {'q': ''})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_admin_works_without_query(logged_client, joboffers_list):
    """
    Test that an empty queryset returns the joboffers reversed
    """
    client = logged_client

    target_url = reverse_lazy('joboffers:admin')

    response = client.get(target_url)

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('id', flat=True)

    joboffers_list.reverse()
    expected_joboffers = [joboffer.id for joboffer in joboffers_list]
    assert list(actual_joboffers) == expected_joboffers


@pytest.mark.django_db
def test_joboffer_admin_filters_by_company_name(logged_client, joboffers_list):
    """
    Test that searching by title2 retrieves only title2 joboffer
    """
    client = logged_client

    target_url = reverse_lazy('joboffers:admin')

    response = client.get(target_url, {'q': JOBOFFER_TITLE2})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2]


@pytest.mark.django_db
def test_joboffer_admin_filters_by_exactly_by_tagname(logged_client, joboffers_list):
    """
    Test that searching by tag retrieves only the offers that match exactly with the tag name
    """
    client = logged_client

    target_url = reverse_lazy('joboffers:admin')

    response = client.get(target_url, {'q': 'tag1'})

    assert response.status_code == 200
    actual_joboffers = response.context_data['object_list'].values_list('title', flat=True)

    assert list(actual_joboffers) == [JOBOFFER_TITLE2, JOBOFFER_TITLE1]
