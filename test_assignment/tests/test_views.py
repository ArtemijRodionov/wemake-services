from django.test import TestCase
from django.urls import reverse

from test_assignment import auth_session


class Auth(TestCase):

    def test_authorize_missing_code(self):
        response = self.client.get(reverse('authorize'), {'state': '321'}, secure=True)
        self.assertEqual(response.status_code, 403)

    def test_authorize_missing_state(self):
        session = self.client.session
        session[auth_session.GithubSession.session_key] = {'state': 123}
        session.save()

        response = self.client.get(reverse('authorize'), {'code': '123'}, secure=True)
        self.assertEqual(response.status_code, 403)
