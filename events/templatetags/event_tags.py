from django import template

from events.models import Event

from datetime import date

register = template.Library()

@register.inclusion_tag('events/next_events.html')
def next_events():
    events = Event.objects.filter(
        start_at__gte=date.today()
    ).order_by(
        '-updated_at'
    )
    return {'events': events}
