# -*- coding: utf-8 -*-

"""Tareas celery del modulo events."""

import datetime
from datetime import (
    datetime,
    timedelta
)

from celery import task
from events.models import Event
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


@task
def notify_events():
    u"""Notificar los eventos que ocurriran durante los próximos siete días."""
    today = datetime.today().date() - timedelta(days=1)
    until = today + timedelta(days=7)
    events = Event.objects.filter(start_at__range=(today, until))

    if events.count() == 0:
        return

    email = EmailMessage(
        subject=_('[PyAr] Eventos en la próxima semana'),
        to=(settings.PYAR_MAILING_LIST, ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        body=render_to_string('events/next_week_events_email.txt', {'events': events})
    )
    email.send(fail_silently=False)
