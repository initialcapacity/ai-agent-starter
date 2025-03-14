import json
from dataclasses import asdict
from typing import List

from agents import function_tool
from openai.types.beta import FunctionTool

from discovery.github_support.github_client import GithubClient


def github_tools(client: GithubClient) -> List[FunctionTool]:
    @function_tool
    def list_repositories_for_organization(organization: str) -> str:
        """Gets a list of repositories for a given organization"""
        org_repositories = client.list_repositories_for_organization(organization)
        return json.dumps([asdict(repo) for repo in org_repositories])

    @function_tool
    def list_repositories_for_user(user: str) -> str:
        """Gets a list of repositories for a given user"""
        user_repositories = client.list_repositories_for_user(user)
        return json.dumps([asdict(repo) for repo in user_repositories])

    @function_tool
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

    @function_tool
    def list_repository_languages(full_name: str) -> str:
        """
        Gets a list of languages for a given repository

        full_name: The full name of the repository, for example: "owner/repo"
        """
        languages = client.list_repository_languages(full_name)
        return json.dumps(languages)

    @function_tool
    def list_repository_contributors(full_name: str) -> str:
        """
        Gets a list of contributors for a given repository

        full_name: The full name of the repository, for example: "owner/repo"
        """
        contributors = client.list_repository_contributors(full_name)
        return json.dumps(contributors)

    return [
        list_repositories_for_organization,
        list_repositories_for_user,
        search_repositories,
        list_repository_languages,
        list_repository_contributors,
    ]
