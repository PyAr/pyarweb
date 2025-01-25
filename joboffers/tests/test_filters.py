import pytest

from pycompanies.tests.factories import CompanyFactory
from ..templatetags.history import (verbose_name, joboffer_verbose_name, joboffer_value,
                                    get_old_field_item, get_new_field_item)
from ..models import HiringType
from .factories import JobOfferFactory

TEST_FIELD_NAME = 'location'
TEST_FIELD_VALUE = 'Capital'
TEST_OLD_VALUE = 'old'
TEST_NEW_VALUE = 'new'
EXPECTED_FIELD_VERBOSE_NAME = 'Lugar'
REMOVED_FIELD_NAME = 'obsolete_field'


@pytest.mark.django_db
def test_verbose_name_for_joboffer():
    """
    Assert that the verbose_name filter works for a joboffer model instance
    """
    joboffer = JobOfferFactory.create()
    result = verbose_name(joboffer, TEST_FIELD_NAME)

    assert result == EXPECTED_FIELD_VERBOSE_NAME


def test_joboffer_verbose_name_for_field_item():
    """
    Assert that the verbose_name filter returns a verbose name for a item key-value pair
    """
    field_item = (TEST_FIELD_NAME, 'sample')
    result = joboffer_verbose_name(field_item)

    assert result == EXPECTED_FIELD_VERBOSE_NAME


def test_joboffer_verbose_name_for_unexistent_field_item():
    """
    Assert that the verbose_name filter returns the same field_name when it is called with
    unexistent field_name
    """
    field_item = (REMOVED_FIELD_NAME, 'sample')
    result = joboffer_verbose_name(field_item)

    assert result == REMOVED_FIELD_NAME


def test_joboffer_value_returns_human_readable_value_for_a_string_field():
    """
    Assert that the joboffer_value filter returns human readable value for a string field
    """
    field_item = (TEST_FIELD_NAME, TEST_FIELD_VALUE)
    result = joboffer_value(field_item)

    assert result == TEST_FIELD_VALUE


def test_joboffer_value_returns_human_readable_for_a_choices_field():
    """
    Assert that the joboffer_value filter returns human readable value for a choices field
    """
    field_item = ('hiring_type', HiringType.COOPERATIVE.value)
    result = joboffer_value(field_item)

    assert result == HiringType.COOPERATIVE.label


def test_joboffer_value_returns_human_readable_update_field_foreign_key_field():
    """
    Assert that the joboffer_value filter returns human readable value for a choices field
    """
    TEST_VALUE = 'random_user'
    field_item = ('modified_by', TEST_VALUE)
    result = joboffer_value(field_item)

    assert result == TEST_VALUE


@pytest.mark.django_db
def test_joboffer_value_returns_human_readable_for_a_foreign_key_field():
    """
    Assert that the joboffer_value filter returns human readable value for a choices field
    """
    company = CompanyFactory.create()
    field_item = ('company', company.id)
    result = joboffer_value(field_item)

    assert result == company


def test_joboffer_value_returns_human_readable_for_a_missing_field():
    """
    Assert that the joboffer_value filter returns human readable value for a field that has been
    removed from the model
    """
    field_item = (REMOVED_FIELD_NAME, TEST_FIELD_VALUE)
    result = joboffer_value(field_item)

    assert result == TEST_FIELD_VALUE


def test_get_old_field_item():
    """
    Test the get_old_field_item filter
    """
    field_update = (TEST_FIELD_NAME, (TEST_OLD_VALUE, TEST_NEW_VALUE))
    result = get_old_field_item(field_update)

    assert result == (TEST_FIELD_NAME, TEST_OLD_VALUE)


def test_get_new_field_item():
    """
    Test the get_new_field_item filter
    """
    field_update = (TEST_FIELD_NAME, (TEST_OLD_VALUE, TEST_NEW_VALUE))
    result = get_new_field_item(field_update)

    assert result == (TEST_FIELD_NAME, TEST_NEW_VALUE)
