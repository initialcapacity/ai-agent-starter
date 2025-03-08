from typing import Protocol, Callable

import mistune
from flask import Blueprint, render_template, request, g
from flask.typing import ResponseReturnValue

from discovery.agent_support.agent import AgentResult
from discovery.auth.requre_authentication import require_authentication
from discovery.github_support.github_client import GithubClient


class AiAgent(Protocol):
    def answer(self, query: str) -> AgentResult:
        ...


def index_page(agent_creator: Callable[[GithubClient], AiAgent]) -> Blueprint:
    page = Blueprint('index_page', __name__)

    @page.get('/')
    @require_authentication
    def index() -> ResponseReturnValue:
        return render_template('index.html')

    @page.post('/')
    @require_authentication
    def query() -> ResponseReturnValue:
        user_query = request.form.get('query')
        agent = agent_creator(GithubClient(g.github_token))
        result = agent.answer(user_query)

        return render_template(
            'response.html',
            query=user_query,
            response=mistune.html(result.response),
            tool_calls=result.tool_calls,
        )

    return page
