import json
from dataclasses import asdict
from typing import List

from explorer.agent_support.tool import Tool, tool
from explorer.github_support.github_client import GithubClient


def github_tools(client: GithubClient) -> List[Tool]:
    @tool()
    def list_repositories_for_organization(organization: str) -> str:
        """Gets a list of repositories for a given organization"""
        org_repositories = client.list_repositories_for_organization(organization)
        return json.dumps([asdict(repo) for repo in org_repositories])

    @tool()
    def list_repositories_for_user(user: str) -> str:
        """Gets a list of repositories for a given user"""
        user_repositories = client.list_repositories_for_user(user)
        return json.dumps([asdict(repo) for repo in user_repositories])

    @tool()
    def list_repository_languages(repository_api_url: str) -> str:
        """Gets a list of languages for a given repository"""
        languages = client.list_repository_languages(repository_api_url)
        return json.dumps(languages)

    @tool()
    def list_repository_contributors(repository_api_url: str) -> str:
        """Gets a list of contributors for a given repository"""
        contributors = client.list_repository_contributors(repository_api_url)
        return json.dumps(contributors)

    return [
        list_repositories_for_organization,
        list_repositories_for_user,
        list_repository_languages,
        list_repository_contributors,
    ]
