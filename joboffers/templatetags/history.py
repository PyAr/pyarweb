from django import template
from django.core.exceptions import FieldDoesNotExist

from ..models import JobOffer


register = template.Library()


@register.filter
def verbose_name(model, field_name):
    """
    Get the verbose name for a given model instance and field name.
    The model must have the get_options() method implemented
    """
    meta = model.get_options()

    field = meta.get_field(field_name)
    return field.verbose_name


@register.filter
def joboffer_verbose_name(field_item):
    """
    Get the verbose name for a field_item (key-value). It returns the same field_name if the field
    is not present in the model anymore. That will be the case of a field removed/renamed in the
    model.
    The model must have the get_options() method implemented
    """
    field_name, _ = field_item
    meta = JobOffer.get_options()
    try:
        field = meta.get_field(field_name)
    except FieldDoesNotExist:
        return field_name
    return field.verbose_name


@register.filter
def joboffer_value(field_item):
    """
    Get the human readable value for a joboffer for a key-value pair.
    """
    field_name, field_value = field_item
    meta = JobOffer.get_options()

    try:
        field = meta.get_field(field_name)
    except FieldDoesNotExist:
        return field_value

    attr_name = field.attname  # Foreign keys use a different attribute name
    joboffer = JobOffer(**{attr_name: field_value})

    display_function = getattr(joboffer, f"get_{field_name}_display", None)

    if display_function:
        return display_function()
    else:
        return getattr(joboffer, field_name)


@register.filter
def get_old_field_item(field_update):
    """
    Get the old key-value for a field_update.
    """
    return (field_update[0], field_update[1][0])


@register.filter
def get_new_field_item(field_update):
    """
    Get the new key-value for a field_update.
    """
    return (field_update[0], field_update[1][1])
