from django import template

from events.models import Event

from django.utils import timezone

register = template.Library()

@register.inclusion_tag('events/next_events.html')
def next_events():
    events = Event.objects.filter(
        end_at__gte=timezone.now()
    ).order_by(
        '-updated_at'
    )
    return {'events': events}
