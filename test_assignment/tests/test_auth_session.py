from unittest.mock import MagicMock

from django.test import TestCase

from test_assignment import auth_session


class GithubSession(TestCase):

    def request(self):
        return MagicMock(url='https://example.com', session=self.client.session)

    def test_auth_url(self):
        """Set `state` parameter to a url and setup session."""
        request = self.request()
        github = auth_session.GithubSession(request)
        url = github.auth_url()

        state = request.session.get(github.session_key, {}).get('state', '')
        self.assertTrue(state, request.session)
        self.assertIn(f'state={state}', url)

    def test_update_token(self):
        """Set a token to session."""
        request = self.request()
        github = auth_session.GithubSession(request)

        # setup session
        github.auth_url()
        # update session
        token = {'access_token': 111, 'token_type': 'bearer'}
        github.session = MagicMock(fetch_token=MagicMock(return_value=token))
        github.update_token()

        self.assertEqual(
            request.session.get(github.session_key, {}).get('token', {}),
            token,
        )
