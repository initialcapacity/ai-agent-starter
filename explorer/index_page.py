from typing import Protocol

import mistune
from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

from explorer.agent_support.agent import AgentResult


class AiAgent(Protocol):
    def answer(self, query: str) -> AgentResult:
        ...


def index_page(agent: AiAgent) -> Blueprint:
    page = Blueprint('index_page', __name__)

    @page.get('/')
    def index() -> ResponseReturnValue:
        return render_template('index.html')

    @page.post('/')
    def query() -> ResponseReturnValue:
        user_query = request.form.get('query')
        result = agent.answer(user_query)

        return render_template(
            'response.html',
            query=user_query,
            response=mistune.html(result.response),
            tool_calls=result.tool_calls,
        )

    return page
