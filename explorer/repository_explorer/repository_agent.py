from openai import OpenAI

from explorer.agent_support.agent import Agent
from explorer.github_support.github_client import GithubClient
from explorer.repository_explorer.github_tools import github_tools


def create_repository_agent(open_ai_client: OpenAI, github_client: GithubClient) -> Agent:
    return Agent(
        client=open_ai_client,
        model="gpt-4o",
        instructions="""
            You are a helpful assistant that can answer a user's questions about GitHub Repositories.
            Use the provided functions to answer the user's questions.
            When possible, prefer to use search functions over list functions to find lists of repositories matching certain
            criteria.
            Provide your answers in markdown format.
        """,
        tools=github_tools(github_client)
    )
