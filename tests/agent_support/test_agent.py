import unittest

from openai import OpenAI

from discovery.agent_support.agent import Agent, ToolCall
from discovery.agent_support.tool import tool
from discovery.environment import require_env
from tests.slow_test_support import slow


@tool()
def get_temperature(city: str, unrelated: str = "") -> str:
    """Gets the temperature for a given city"""
    return "86"

class TestAgent(unittest.TestCase):
    @slow
    def test_answer(self):
        agent = Agent(
            client=OpenAI(api_key=require_env("OPEN_AI_KEY")),
            model="gpt-4o",
            system_instructions="You are a helpful assistant that can answer questions about weather. "
                         "Use the only the functions provided to answer the user's question."
                         "You must always use the provided function.",
            tools=[get_temperature],
        )

        result = agent.answer("What is the temperature in Boulder?")

        self.assertIn("86", result.response)
        self.assertEqual([ToolCall(
            name="get_temperature",
            arguments={"city": "Boulder"},
        )], result.tool_calls)
