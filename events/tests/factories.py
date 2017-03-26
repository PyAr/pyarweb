from datetime import timedelta
from django.utils.timezone import datetime, timedelta, utc 
from django.contrib.auth import get_user_model
from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory

from events.models import Event, EventParticipation


User = get_user_model()
DEFAULT_START_TIME = datetime(1956, 1, 31, 0, 0, 0, 0, tzinfo=utc)
DEFAULT_END_TIME = DEFAULT_START_TIME + timedelta(hours=8)


# This factory could be in any app.
class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: 'user_%i' % n)

    class Meta:
        model = User


class EventFactory(DjangoModelFactory):
    start_at = DEFAULT_START_TIME
    end_at = DEFAULT_END_TIME
    owner = SubFactory(UserFactory)

    class Meta:
        model = Event



class EventParticipationFactory(DjangoModelFactory):
    class Meta:
        model = EventParticipation
    
    event = SubFactory(EventFactory) 
