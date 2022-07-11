import os
import inspect

from django.conf import settings
from django.template import Context, Template
from django.utils.module_loading import import_string

from ..models import JobOffer


class Publisher:
    """Base class for Publishing classes like Twitter, Facebook, etc."""
    name = None
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    def _render_offer(self, job_offer: 'JobOffer'):
        """Render JobOffer using a custom template for each Publisher."""
        # First, we need to get the file path for the class
        # inheriting from the baseclass (not the current __file__)
        class_file = inspect.getfile(self.__class__)
        path = os.path.dirname(class_file)
        template_path = os.path.join(path, 'template.html')
        with open(template_path) as template_file:
            template_content = template_file.read()

        template = Template(template_content)
        context = Context({'job_offer': job_offer})
        return template.render(context)

    def _push_to_api(self, message: str, title: str):
        """This method should implement what is necessary to interact with each API."""
        raise NotImplementedError

    def publish(self, job_offer: 'JobOffer'):
        """Render and send the JobOffer to the publisher,
        using the API configured in push_to_api method."""
        message = self._render_offer(job_offer)
        status = self._push_to_api(message, job_offer.title, job_offer.get_full_url())

        if status in (200, 201):
            return self.RESULT_OK
        else:
            return self.RESULT_BAD


def publish_offer(job_offer: 'JobOffer', publishers: list = None):
    """Publish a job_offer into the given list of publishers."""
    failed = []

    if publishers:
        for publisher in publishers:
            result = publisher().publish(job_offer)

            if result != Publisher.RESULT_OK:
                failed.append(publisher.name)
    else:
        raise ValueError

    return failed


def publish_to_all_social_networks(joboffer):
    """
    Send the joboffer to all the configured social networks.
    """
    publishers = [import_string(p) for p in settings.SOCIAL_NETWORKS_PUBLISHERS]
    return publish_offer(joboffer, publishers)
