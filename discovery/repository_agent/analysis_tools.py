from discovery.local_repo_support.local_repo_client import LocalRepoClient
from typing import List

from discovery.agent_support.tool import Tool, tool
from discovery.local_repo_support.scc_client import SccClient


def analysis_tools(local_repo_client: LocalRepoClient, scc_client: SccClient) -> List[Tool]:
    @tool()
    def is_repositories_checked_out(repository_api_url: str) -> str:
        """Check if a repository with the given url is checked out"""
        return str(local_repo_client.is_repositories_checked_out(repository_api_url))

    @tool()
    def check_out_repositories(repository_api_url: str) -> str:
        """Check out a repository for a given url"""
        return "Done"

    @tool()
    def analysis_code(repository_api_url: str) -> str:
        """
        Analyze and produce a report for a repository.
        The repository needs to be checked out before this can be run.

        The report includes the following:
        - The number of files that use a given language
        - The sum complexity of all files using a given language
        - The breakdown of number of files, lines, comments, and black lines by a given language
        - The total number of files, lines, comments, and black lines across all languages
        - The estimated cost to develop
        - The estimated schedule effort
        - The estimated people required

        repository_api_url: Url for the repository to analyze
        """
        return scc_client.analyzeCode(repository_api_url)

    return [
        is_repositories_checked_out,
        check_out_repositories,
        analysis_code,
    ]