import unittest

from explorer.agent_support.tool import tool, Argument


@tool()
def some_tool(username: str, count: int, done: bool = False) -> str:
    """A helpful description"""
    return f"Hello {username}, {count}, {done}"

class TestTool(unittest.TestCase):
    def test_tool_attributes(self):
        self.assertEqual("some_tool", some_tool.name)
        self.assertEqual("A helpful description", some_tool.description)
        self.assertEqual("Hello fred, 3, True", some_tool.action("fred", 3, True))
        self.assertEqual([
            Argument(name="username", type="string", required=True),
            Argument(name="count", type="number", required=True),
            Argument(name="done", type="boolean", required=False),
        ], some_tool.arguments)

    def test_tool_schema(self):
        self.assertEqual({
            "type": "function",
            "function": {
                "name": "some_tool",
                "description": "A helpful description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "count": {"type": "number"},
                        "done": {"type": "boolean"},
                    },
                    "required": ["username", "count"],
                }
            }
        }, some_tool.schema())
