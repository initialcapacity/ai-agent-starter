from typing import Callable

from openai import OpenAI

from discovery.agent_support.agent import Agent
from discovery.github_support.github_client import GithubClient
from discovery.repository_agent.github_tools import github_tools


def repository_agent_creator(open_ai_client: OpenAI) -> Callable[[GithubClient], Agent]:
    return lambda github_client: Agent(
        client=open_ai_client,
        model="gpt-4o-mini",
        system_instructions="""
            You are a helpful assistant that can answer a user's questions about GitHub Repositories.
            Use the provided functions to answer the user's questions.
            When possible, prefer to use search functions over list functions to find lists of repositories matching certain
            criteria.
            Provide your answers in markdown format.
        """,
        tools=github_tools(github_client)
    )
