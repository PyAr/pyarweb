import factory
import pytest

from django.test import Client
from django.urls import reverse_lazy
from django.contrib.messages import get_messages as contrib_get_messages

from events.tests.factories import UserFactory, DEFAULT_USER_PASSWORD

from .factories import CompanyFactory, UserCompanyProfileFactory
from ..models import Company


ERROR_USER_DOES_NOT_EXIST = 'Le usuarie que ingresó no existe.'
USER_ASSOCIATED_CORRECTLY = 'Le usuarie fue asociade correctamente.'

ADMIN_URL = reverse_lazy('companies:admin')


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


@pytest.fixture(name='user_company_profile')
def create_user_company_profile():
    """
    Fixture with a dummy UserCompanyProfileFactory
    """
    return UserCompanyProfileFactory.create()


@pytest.mark.django_db
def test_associate_unexisting_user(logged_client):

    company = CompanyFactory.create()
    ASSOCIATE_URL = reverse_lazy('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': 'pepito'})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert message == ERROR_USER_DOES_NOT_EXIST


@pytest.mark.django_db
def test_associate_user_in_company(logged_client):

    company = CompanyFactory.create()
    user = UserFactory.create()

    ASSOCIATE_URL = reverse_lazy('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert message == USER_ASSOCIATED_CORRECTLY


@pytest.mark.django_db
def test_associate_user_already_in_company(logged_client):

    company = CompanyFactory.create()
    user = UserFactory.create()
    user_company = UserCompanyProfileFactory.create(company=company, user=user)

    ERROR_USER_ALREADY_IN_COMPANY = f'Le usuarie que desea vincular ya pertenece a {user_company.company}'

    ASSOCIATE_URL = reverse_lazy('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert message == ERROR_USER_ALREADY_IN_COMPANY


@pytest.mark.django_db
def test_associate_user_in_other_company(logged_client):

    user = UserFactory.create()
    company = CompanyFactory.create(name='company_1')
    other_company = CompanyFactory.create(name='company_2')
    UserCompanyProfileFactory.create(company=other_company, user=user)

    ERROR_USER_IN_OTHER_COMPANY = f'Le usuarie que ingresó esta vinculade a {other_company}.'

    ASSOCIATE_URL = reverse_lazy('companies:associate', kwargs={'company': company.id})

    response = logged_client.post(ASSOCIATE_URL, data={'username': user.username})
    message = get_plain_messages(response)[0]

    assert 302 == response.status_code
    assert ADMIN_URL == response.url
    assert message == ERROR_USER_IN_OTHER_COMPANY


@pytest.mark.django_db
def test_company_admin_with_no_logged_user_should_redirect(client):

    response = client.get(ADMIN_URL)

    assert 302 == response.status_code


@pytest.mark.django_db
def test_company_admin_with_logged_user_should_not_redirect(logged_client):

    response = logged_client.get(ADMIN_URL)

    assert 200 == response.status_code


@pytest.mark.django_db
def test_company_admin_should_have_two_companies_in_context(logged_client):

    company_1 = CompanyFactory.create(name='company_1')
    company_2 = CompanyFactory.create(name='company_2')
    COMPANY_ADMIN_URL = reverse_lazy('companies:admin')

    response = logged_client.get(COMPANY_ADMIN_URL, data={'empresa': 'company'})

    assert 200 == response.status_code
    assert 2 == len(response.context['companies'])
    assert company_1 == response.context['companies'][0]
    assert company_2 == response.context['companies'][1]


@pytest.mark.django_db
def test_company_admin_should_have_one_company_in_context(logged_client):

    company_1 = CompanyFactory.create(name='company_1')
    COMPANY_ADMIN_URL = reverse_lazy('companies:admin')

    response = logged_client.get(COMPANY_ADMIN_URL, data={'empresa': 'company'})

    assert 200 == response.status_code
    assert 1 == len(response.context['companies'])
    assert company_1 == response.context['companies'][0]
