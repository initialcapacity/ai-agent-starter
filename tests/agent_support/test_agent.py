import unittest

from openai import OpenAI

from explorer.agent_support.agent import Agent
from explorer.agent_support.tool import tool
from explorer.environment import require_env
from tests.slow_test_support import slow


@tool()
def get_temperature(city: str) -> str:
    """Gets the temperature for a given city"""
    return "86"

class TestAgent(unittest.TestCase):
    @slow
    def test_answer(self):
        agent = Agent(
            client=OpenAI(api_key=require_env("OPEN_AI_KEY")),
            model="gpt-4o",
            instructions="You are a helpful assistant that can answer questions about weather. "
                         "Use the only the functions provided to answer the user's question."
                         "You must always use the provided function.",
            tools=[get_temperature],
        )

        answer = agent.answer("What is the temperature in Boulder?")

        self.assertIn("86", answer)
