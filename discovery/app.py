import logging

from flask import Flask
from openai import OpenAI

from discovery.auth.allowed_emails import AllowedEmails
from discovery.authentication_page import authentication_page
from discovery.environment import Environment
from discovery.github_support.github_oauth_client import GithubOAuthClient
from discovery.index_page import index_page
from discovery.oauth_api import oauth_api
from discovery.repository_agent.repository_agent import repository_agent_creator

logger = logging.getLogger(__name__)


def create_app(env: Environment = Environment.from_env()):
    app = Flask(__name__)
    app.secret_key = env.flask_secret_key

    open_ai_client = OpenAI(api_key=env.open_ai_key)
    agent_creator = repository_agent_creator(open_ai_client)

    app.register_blueprint(index_page(agent_creator))

    if env.github_oauth_enabled:
        oauth_client = GithubOAuthClient(client_id=env.github_client_id, client_secret=env.github_client_secret)
        allowed_emails = AllowedEmails(domains=env.allowed_domains, addresses=env.allowed_addresses)

        app.register_blueprint(oauth_api(oauth_client, allowed_emails))
    else:
        app.register_blueprint(authentication_page())

    return app
