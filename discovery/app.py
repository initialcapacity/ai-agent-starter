import logging

from flask import Flask
from openai import OpenAI

from discovery.environment import Environment
from discovery.github_support.github_client import GithubClient
from discovery.index_page import index_page
from discovery.repository_agent.repository_agent import create_repository_agent

logger = logging.getLogger(__name__)


def create_app(env: Environment = Environment.from_env()):
    app = Flask(__name__)
    open_ai_client = OpenAI(api_key=env.open_ai_key)
    github_client = GithubClient(access_token=env.github_token)

    agent = create_repository_agent(open_ai_client, github_client)

    app.register_blueprint(index_page(agent))

    return app
