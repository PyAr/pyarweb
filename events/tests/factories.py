from django.utils.timezone import datetime, timedelta, utc
from django.contrib.auth import get_user_model
from factory import SubFactory, Faker, PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory

from events.models import Event, EventParticipation


User = get_user_model()
DEFAULT_START_TIME = datetime(1956, 1, 31, 0, 0, 0, 0, tzinfo=utc)
DEFAULT_END_TIME = DEFAULT_START_TIME + timedelta(hours=8)
DEFAULT_USER_PASSWORD = 'secret'


# This factory could be in any app.
class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: f'user{n}')
    password = PostGenerationMethodCall('set_password', DEFAULT_USER_PASSWORD)

    class Meta:
        model = User
        # Warning!: Using the factory to get an already existing user logs out the user in the
        # session :(, maybe because the password setting
        django_get_or_create = ('username',)


class EventFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=4)
    description = Faker('text')
    address = Faker('address')
    place = Faker('sentence', nb_words=2)
    start_at = DEFAULT_START_TIME
    end_at = DEFAULT_END_TIME
    owner = SubFactory(UserFactory)

    class Meta:
        model = Event


class FutureEventFactory(EventFactory):
    start_at = datetime.now(tz=utc) + timedelta(days=1)
    end_at = datetime.now(tz=utc) + timedelta(days=2)

    class Meta:
        model = Event


class EventParticipationFactory(DjangoModelFactory):
    class Meta:
        model = EventParticipation

    event = SubFactory(EventFactory)
