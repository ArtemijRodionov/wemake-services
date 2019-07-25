import abc
from unittest.mock import MagicMock

from django.conf import settings
from requests_oauthlib import OAuth2Session


class AuthSession(abc.ABC):

    def __init__(self, request):
        self.request = request

    @abc.abstractproperty
    def authorized(self):
        pass

    @abc.abstractproperty
    def client(self):
        pass

    @abc.abstractmethod
    def auth_url(self):
        pass

    @abc.abstractmethod
    def update_token(self):
        pass


class GithubSession(AuthSession):

    session_key = 'github_oauth'

    def __init__(self, request):
        super().__init__(request)
        self.session = OAuth2Session(
            settings.GITHUB_CLIENT_ID,
            **request.session.get(self.session_key, {}),
        )

    @property
    def authorized(self):
        return self.session.authorized

    @property
    def client(self):
        return self.session

    def auth_url(self):
        url, state = self.session.authorization_url(
            'https://github.com/login/oauth/authorize'
        )
        self.request.session[self.session_key] = {'state': state}
        return url

    def update_token(self):
        token = self.session.fetch_token(
            'https://github.com/login/oauth/access_token',
            client_secret=settings.GITHUB_CLIENT_SECRET,
            authorization_response=self.request.build_absolute_uri(),
        )
        self.request.session[self.session_key]['token'] = token
        self.request.session.modified = True
