import unittest

from discovery.agent_support.agent import AgentResult, ToolCall
from discovery.index_page import index_page
from tests.blueprint_test_support import test_client


class FakeAgent:
    def answer(self, question: str) -> AgentResult:
        return AgentResult(
            response="Some response",
            tool_calls=[
                ToolCall(name="some_tool", arguments={"some_argument": "some_value"}),
            ],
        )


class TestIndexPage(unittest.TestCase):
    def setUp(self):
        self.client = test_client(index_page(lambda token: FakeAgent()), authenticated=True)

    def test_index_page(self):
        response = self.client.get("/")

        self.assertEqual(200, response.status_code)
        self.assertIn("What would you like to know?", response.text)

    def test_query(self):
        response = self.client.post("/", data={"query": "What is your response?"})

        self.assertEqual(200, response.status_code)
        self.assertIn("Some response", response.text)
        self.assertIn("some_tool", response.text)
        self.assertIn("some_argument", response.text)
        self.assertIn("some_value", response.text)
