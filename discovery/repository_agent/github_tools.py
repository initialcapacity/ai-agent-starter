import json
from dataclasses import asdict
from typing import List

from discovery.agent_support.tool import Tool, tool
from discovery.github_support.github_client import GithubClient


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
    def search_repositories(owner: str, owner_type: str, query: str = None, language: str = None) -> str:
        """
        Search for repositories matching the criteria given in the arguments

        owner: The owner of the repositories to search for
        owner_type: The type of owner. Must be either user or org
        query: The query to search for (Optional: pass in None if not needed)
        language: The programming language to search for (Optional: pass in None if not needed)
        """

        repositories = client.search_repositories(owner, owner_type, query, language)
        return json.dumps([asdict(repo) for repo in repositories])

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
        search_repositories,
        list_repository_languages,
        list_repository_contributors,
    ]
