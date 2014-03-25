# -*- coding: utf-8 -*-

import requests
from urllib.parse import urljoin


class API(object):
    """Base API object."""

    def __init__(self, url):
        self.url = url


class Resource(object):

    def __init__(self, path, api, **kwargs):
        self.method = kwargs.get('method')
        self.path = path
        self.api = api
        self.url = urljoin(self.api.url, self.path)

    def _make_request(self):
        """Make a request with requests and return the response."""
        if self.method.upper() == 'GET':
            response = requests.get(self.url)

        return response

    def json(self):
        """Return the results from the API Request as json."""
        response = self._make_request()
        return response.json()


class BaseClient(object):
    """Base class for api clients."""

    def __init__(self):
        self._resources = dict()

    def get(self, resource, **kwargs):
        if not resource in self._resources:
            kwargs['method'] ='GET'
            self._resources[resource] = \
                Resource(resource, api=self.api, **kwargs)
        return self._resources[resource]


class GithubClient(BaseClient):
    """Github API v3 client."""

    def __init__(self, url):
        self.api = API(url)
        super(GithubClient, self).__init__()


class BitbucketClient(BaseClient):
    """BitbucketClient, to be implemented."""


github = GithubClient('https://api.github.com')
