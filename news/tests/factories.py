from factory import SubFactory, Sequence, post_generation
from factory.django import DjangoModelFactory

from events.tests.factories import UserFactory
from news.models import NewsArticle


class NewsArticleFactory(DjangoModelFactory):
    class Meta:
        model = NewsArticle

    owner = SubFactory(UserFactory)
    title = Sequence(lambda n: 'news_title_%i' % n)

    @post_generation
    def set_created(obj, create, extracted, **kwargs):
        """
        Update the creation time of the built instance. As it is an auto-generated field, we must
        set its value after creation.

        To use: NewsArticleFactory(set_created='1985-10-26 09:00Z')

        """
        if extracted:
            obj.created = extracted
            obj.save()
