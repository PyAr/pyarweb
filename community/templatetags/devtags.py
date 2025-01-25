from django.template import Library
from lxml import etree
from django.contrib.auth.models import Group

register = Library()


@register.filter
def get_range(value):
    """
        Filter - returns a list containing range made from given value
        Usage (in template):

        <ul>{% for i in 3|get_range %}
            <li>{{ i }}. Do something</li>
        {% endfor %}</ul>

        Results with the HTML:
        <ul>
            <li>0. Do something</li>
            <li>1. Do something</li>
            <li>2. Do something</li>
        </ul>

        Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter
def html2text(html):
    if html:
        return etree.tostring(
            etree.HTML(html),
            encoding='utf8',
            method='text'
        ).decode('utf8')
    return ''


@register.filter
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
