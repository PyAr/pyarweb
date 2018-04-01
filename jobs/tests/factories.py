from factory import SubFactory, Sequence, post_generation
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from jobs.models import Job


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job

    owner = SubFactory(UserFactory)
    title = Sequence(lambda n: 'job_title_%i' % n)

    @post_generation
    def set_created(obj, create, extracted, **kwargs):
        """
        Update the creation time of the built instance. As it is an auto-generated field, we must
        set its value after creation.

        To use: JobFactory(set_created='1985-10-26 09:00Z')

        """
        if extracted:
            obj.created = extracted
            obj.save()
