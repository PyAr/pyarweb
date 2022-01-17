import pytest
from django.contrib.auth.models import AnonymousUser
from django.template import Template, Context

from ..publisher import Publisher, publish_offer
from ..models import OfferState
from .factories import JobOfferFactory


DUMMY_TEMPLATE = "<h1>{job_offer.slug}</h1> <p>{job_offer.company.name}</p>"


class DummyPublisher(Publisher):
    @classmethod
    def publish(cls, job_offer):
        result = cls._render_offer(job_offer)
        breakpoint()
        print(result)


    @classmethod
    def _render_offer(cls, job_offer):
        template = Template(DUMMY_TEMPLATE)
        context = Context({'job_offer': job_offer})
        return template.render(context)


@pytest.mark.django_db
def test_publish_offer():
    user = AnonymousUser()
    joboffer = JobOfferFactory.create(state=OfferState.DEACTIVATED)

    publish_offer(joboffer, (DummyPublisher, ))
