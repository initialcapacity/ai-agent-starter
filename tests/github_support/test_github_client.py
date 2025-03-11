import unittest
import responses

from discovery.github_support.github_client import GithubClient, Repository, GithubUser


class TestGithubClient(unittest.TestCase):
    def setUp(self):
        self.repo_dict = {
            "name": "some_repo",
            "full_name": "some_organization/some_repo",
            "html_url": "https://example.com/some_owner/some_repo",
            "url": "https://api.example.com/some_owner/some_repo",
            "description": "Just some repo",
            "private": False,
            "stargazers_count": 12,
            "watchers_count": 13,
            "forks_count": 14,
        }
        self.client = GithubClient("some_access_token")

    @responses.activate
    def get_user(self):
        responses.add(
            responses.GET,
            "https://api.github.com/user",
            json={"login": "some_user"},
            status=200,
        )

        result = self.client.get_user()

        self.assertEqual(GithubUser("some_user"), result)

    @responses.activate
    def get_emails(self):
        responses.add(
            responses.GET,
            "https://api.github.com/user/emails",
            json=[
                {"email": "test@example.com", "verified": True},
                {"email": "unverified@example.com", "verified": False},
                {"email": "another@example.com", "verified": True},
            ],
            status=200,
        )

        result = self.client.get_emails()

        self.assertEqual(["test@example.com", "another@example.com"], result)

    @responses.activate
    def test_list_repositories_for_organization(self):
        responses.add(
            responses.GET,
            "https://api.github.com/orgs/some_organization/repos",
            json=[self.repo_dict],
            status=200,
        )

        result = self.client.list_repositories_for_organization("some_organization")

        self.assertEqual(1, len(responses.calls))
        self.assertEqual("Bearer some_access_token", responses.calls[0].request.headers["Authorization"])
        self.assertEqual("application/vnd.github+json", responses.calls[0].request.headers["Accept"])
        self.assertEqual("2022-11-28", responses.calls[0].request.headers["X-GitHub-Api-Version"])

        self.assertEqual([
            Repository(
                name="some_repo",
                full_name="some_organization/some_repo",
                html_url="https://example.com/some_owner/some_repo",
                api_url="https://api.example.com/some_owner/some_repo",
                description="Just some repo",
                private=False,
                stars=12,
                watching=13,
                forks=14,
            )
        ], result)

    @responses.activate
    def test_list_repositories_for_user(self):
        responses.add(
            responses.GET,
            "https://api.github.com/users/some_user/repos",
            json=[self.repo_dict],
            status=200,
        )

        result = self.client.list_repositories_for_user("some_user")

        self.assertEqual([
            Repository(
                name="some_repo",
                full_name="some_organization/some_repo",
                html_url="https://example.com/some_owner/some_repo",
                api_url="https://api.example.com/some_owner/some_repo",
                description="Just some repo",
                private=False,
                stars=12,
                watching=13,
                forks=14,
            )
        ], result)

    @responses.activate
    def test_search_repositories(self):
        responses.add(
            responses.GET,
            "https://api.github.com/search/repositories",
            json={
                "items": [self.repo_dict]
            },
            status=200,
        )

        result = self.client.search_repositories(
            owner="some_organization",
            owner_type="org",
            language="kotlin",
        )

        self.assertEqual(1, len(responses.calls))
        self.assertEqual("/search/repositories?q=org:some_organization%20language:kotlin",
                         responses.calls[0].request.path_url)

        self.assertEqual([
            Repository(
                name="some_repo",
                full_name="some_organization/some_repo",
                html_url="https://example.com/some_owner/some_repo",
                api_url="https://api.example.com/some_owner/some_repo",
                description="Just some repo",
                private=False,
                stars=12,
                watching=13,
                forks=14,
            )
        ], result)

    @responses.activate
    def test_list_repository_languages(self):
        responses.add(
            responses.GET,
            "https://api.example.com/some_repo/languages",
            json={
                "python": 100,
                "html": 50,
                "css": 50,
            },
            status=200,
        )

        result = self.client.list_repository_languages("https://api.example.com/some_repo")

        self.assertCountEqual(["python", "html", "css"], result)

    @responses.activate
    def test_list_repository_contributors(self):
        responses.add(
            responses.GET,
            "https://api.example.com/some_repo/contributors",
            json=[
                {"login": "fred"},
                {"login": "mary"},
                {"login": "kate"},
            ],
            status=200,
        )

        result = self.client.list_repository_contributors("https://api.example.com/some_repo")

        self.assertCountEqual(["fred", "mary", "kate"], result)
