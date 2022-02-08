import os

from django.template import Context, Template

from ..models import JobOffer


class Publisher:
    """Base class for Publishing classes like Twitter, Facebook, etc."""
    name = None
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        raise NotImplementedError

    @classmethod
    def _render_offer(cls, job_offer: 'JobOffer'):
        path = os.path.dirname(__file__)
        template_path = os.path.join(path, 'template.html')
        with open(template_path) as template_file:
            template_content = template_file.read()

        template = Template(template_content)
        context = Context({'job_offer': job_offer})
        return template.render(context)


def publish_offer(job_offer: 'JobOffer', publishers: list = None):
    """Publish a job_offer into the given list of publishers."""
    results = {}

    if publishers:
        for publisher in publishers:
            results[publisher.name] = publisher.publish(job_offer)
    else:
        raise ValueError

    return results
