import unittest

import responses
from flask import session

from discovery.authentication_page import authentication_page
from tests.blueprint_test_support import test_client


class TestAuthenticationPage(unittest.TestCase):
    def test_index_page(self):
        client = test_client(authentication_page(), authenticated=False)

        response = client.get("/login")

        self.assertEqual(200, response.status_code)
        self.assertIn("Enter your GitHub Token", response.text)

    @responses.activate
    def test_login(self):
        client = test_client(authentication_page(), authenticated=False)
        responses.add(
            responses.GET,
            "https://api.github.com/user",
            json={"login": "a_user"},
            status=200,
        )

        with client:
            response = client.post("/login", data={"token": "a_token"})

            self.assertEqual(302, response.status_code)
            self.assertEqual("/", response.location)
            self.assertEqual("a_user", session["username"])
            self.assertEqual("a_token", session["github_token"])

    def test_logout(self):
        client = test_client(authentication_page(), authenticated=True)

        with client:
            response = client.get("/logout")

            self.assertEqual(302, response.status_code)
            self.assertEqual("/login", response.location)
            self.assertNotIn("username", session)
            self.assertNotIn("github_token", session)
