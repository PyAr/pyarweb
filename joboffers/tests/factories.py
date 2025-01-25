from factory import Faker, SubFactory, fuzzy, post_generation
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from joboffers.models import (CommentType, EventType, Experience, HiringType, JobOffer,
                              JobOfferComment, JobOfferAccessLog, Remoteness)
from pycompanies.tests.factories import CompanyFactory


class JobOfferFactory(DjangoModelFactory):
    class Meta:
        model = JobOffer
        django_get_or_create = ('title', )

    title = fuzzy.FuzzyText(length=20)
    company = SubFactory(CompanyFactory)
    location = Faker('address')
    contact_mail = Faker('email')
    contact_phone = Faker('phone_number')
    contact_url = Faker('url')
    experience = fuzzy.FuzzyChoice(Experience.values)
    remoteness = fuzzy.FuzzyChoice(Remoteness.values)
    # tags
    hiring_type = fuzzy.FuzzyChoice(HiringType.values)
    salary = Faker('pricetag')
    short_description = Faker('paragraph')
    description = Faker('paragraph')

    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def set_created(obj, create, extracted, **kwargs):
        """
        Update the creation time of the built instance. As it is an auto-generated field, we must
        set its value after creation.

        To use: JobFactory(set_created='1985-10-26 09:00Z')

        """
        if extracted:
            obj.created_at = extracted
            obj.save()

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.tags.add(group)


class JobOfferCommentFactory(DjangoModelFactory):
    class Meta:
        model = JobOfferComment

    created_by = SubFactory(UserFactory)
    comment_type = fuzzy.FuzzyChoice(CommentType.values)
    text = Faker('sentence')
    created_by = SubFactory(UserFactory)
    joboffer = SubFactory(JobOfferFactory)


class JobOfferAccessLogFactory(DjangoModelFactory):
    class Meta:
        model = JobOfferAccessLog

    joboffer = SubFactory(JobOfferFactory)
    month_and_year = fuzzy.FuzzyInteger(low=202101, high=202401010)
    event_type = fuzzy.FuzzyChoice(EventType.values)
