import logging
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class Repository:
    name: str
    full_name: str
    api_url: str
    html_url: str
    description: str


logger = logging.getLogger(__name__)


class GithubClient(object):
    def __init__(self, access_token: str):
        self.request_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def list_repositories_for_organization(self, organization: str) -> List[Repository]:
        response = requests.get(f"https://api.github.com/orgs/{organization}/repos", headers=self.request_headers)
        if response.status_code != 200:
            logger.error(f"Failed to get repositories for organization {organization}: {response.text}")
            return []

        return [self.__repo_from_json(repo) for repo in response.json()]

    def list_repositories_for_user(self, user: str) -> List[Repository]:
        response = requests.get(f"https://api.github.com/user/{user}/repos", headers=self.request_headers)
        if response.status_code != 200:
            logger.error(f"Failed to get repositories for user {user}: {response.text}")
            return []

        return [self.__repo_from_json(repo) for repo in response.json()]

    def list_repository_languages(self, repository_api_url: str) -> List[str]:
        response = requests.get(f"{repository_api_url}/languages", headers=self.request_headers)
        if response.status_code != 200:
            logger.error(f"Failed to get languages for {repository_api_url}: {response.text}")
            return []

        return [key for key in response.json().keys()]

    def list_repository_contributors(self, repository_api_url: str) -> List[str]:
        response = requests.get(f"{repository_api_url}/contributors", headers=self.request_headers)
        if response.status_code != 200:
            logger.error(f"Failed to get contributors for {repository_api_url}: {response.text}")
            return []

        return [user["login"] for user in response.json()]

    @staticmethod
    def __repo_from_json(repo):
        return Repository(
            name=repo["name"],
            full_name=repo["full_name"],
            html_url=repo["html_url"],
            api_url=repo["url"],
            description=repo["description"],
        )
