import json
import logging
from dataclasses import dataclass
from typing import List

from openai import OpenAI

from discovery.agent_support.tool import Tool

logger = logging.getLogger(__name__)


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, any]


@dataclass
class AgentResult:
    response: str
    tool_calls: List[ToolCall]


class Agent:
    def __init__(self, client: OpenAI, model: str, instructions: str, tools: List[Tool]):
        self.client = client
        self.tools = tools
        self.assistant_id = client.beta.assistants.create(
            instructions=instructions,
            model=model,
            tools=[tool.schema() for tool in tools]
        ).id

    def answer(self, question: str) -> AgentResult:
        thread = self.client.beta.threads.create()
        tool_calls = []
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
        )

        run = self.client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=self.assistant_id)
        while run.status != "completed":
            logger.debug(f"status %s", run.status)
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                logger.debug(f"calling %s with args %s", tool_name, arguments)

                tool = next((tool for tool in self.tools if tool.name == tool_name), None)
                if tool is None:
                    raise Exception(f"No tool found with name {tool_name}")

                tool_calls.append(ToolCall(name=tool_name, arguments=arguments))
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": tool.action(**arguments),
                })

            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs,
            )

        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        return AgentResult(
            response=messages.data[0].content[0].text.value,
            tool_calls=tool_calls,
        )
