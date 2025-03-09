import unittest

import responses

from discovery.github_support.github_oauth_client import GithubOAuthClient
from tests.logging_support import disable_logging


class TestGithubOAuthClient(unittest.TestCase):
    def setUp(self):
        self.client = GithubOAuthClient(client_id='some_client_id', client_secret='some_client_secret')

    def test_auth_url(self):
        auth_url = self.client.auth_url()
        self.assertEqual(
            'https://github.com/login/oauth/authorize?client_id=some_client_id&scope=read%3Auser%2Cuser%3Aemail%2Crepo',
            auth_url
        )

    @responses.activate
    def test_fetch_access_token(self):
        token_endpoint = responses.post('https://github.com/login/oauth/access_token', json={'access_token': 'some_access_token'})

        access_token = self.client.fetch_access_token('some_code')

        self.assertEqual('some_access_token', access_token)
        self.assertEqual(1, token_endpoint.call_count)
        recorded_request = responses.calls[0].request
        self.assertEqual(
            "client_id=some_client_id&client_secret=some_client_secret&code=some_code",
            recorded_request.body
        )

    @responses.activate
    def test_fetch_access_token_bad_request(self):
        responses.post('https://github.com/login/oauth/access_token', status=400)

        access_token = self.client.fetch_access_token('some_code')

        self.assertIsNone(access_token)

    @responses.activate
    def test_read_user_info_from_token(self):
        token_endpoint = responses.post('https://api.github.com/applications/some_client_id/token', json={'user': {"login": "some_user"}})
        emails_endpoint = responses.get('https://api.github.com/user/emails', json=[{"email": "test@example.com", "verified": True}])

        user_info = self.client.read_user_info_from_token("some_token")

        self.assertEqual("some_user", user_info.username)
        self.assertEqual(["test@example.com"], user_info.emails)
        self.assertEqual(1, token_endpoint.call_count)
        self.assertEqual('{"access_token": "some_token"}', token_endpoint.calls[0].request.body)
        self.assertEqual(1, emails_endpoint.call_count)
        self.assertEqual("Bearer some_token", emails_endpoint.calls[0].request.headers["Authorization"])

    @disable_logging
    @responses.activate
    def test_read_email_from_token_bad_request(self):
        responses.post('https://api.github.com/applications/some_client_id/token', status=400)

        email = self.client.read_user_info_from_token('some_token')

        self.assertIsNone(email)
