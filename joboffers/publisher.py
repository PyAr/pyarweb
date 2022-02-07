class Publisher:
    """Abstract class for Publishing classes like Twitter, Facebook, etc."""
    name = None
    RESULT_OK = 'ok'
    RESULT_BAD = 'bad'

    @classmethod
    def publish(cls, job_offer: 'JobOffer'):
        raise NotImplementedError

    @classmethod
    def _render_offer(cls, job_offer: 'JobOffer'):
        raise NotImplementedError


def publish_offer(job_offer: 'JobOffer', publishers: list = None):
    """Publish a job_offer into the given list of publishers."""
    results = {}

    if publishers:
        for publisher in publishers:
            results[publisher.name] = publisher.publish(job_offer)
    else:
        raise ValueError

    return results
