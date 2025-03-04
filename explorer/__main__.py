from openai import OpenAI

from explorer.agent_support.agent import Agent
from explorer.environment import Environment
from explorer.github_support.github_client import GithubClient
from explorer.github_tools import github_tools

env = Environment.from_env()
openai_client = OpenAI(api_key=env.open_ai_key)
github_client = GithubClient(access_token=env.github_token)

github_agent = Agent(
    client=openai_client,
    model="gpt-4o",
    instructions="You are a helpful assistant that can answer a user's questions about GitHub Repositories. "
                 "Use the provided functions to answer the user's questions.",
    tools=github_tools(github_client),
)

response = github_agent.answer("Who contributes to Python repositories in the initialcapacity organization?")
print(response)
