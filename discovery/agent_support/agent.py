import json
import logging
from dataclasses import dataclass
from typing import List

from openai import OpenAI
from openai.types.responses import EasyInputMessageParam, Response, ResponseFunctionToolCallParam, \
    ResponseFunctionToolCall
from openai.types.responses.response_input_param import ResponseInputParam, FunctionCallOutput

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
    def __init__(self, client: OpenAI, model: str, system_instructions: str, tools: List[Tool]):
        self.client = client
        self.model = model
        self.instructions = system_instructions
        self.tools = tools
        self.tool_params = [tool.tool_param() for tool in tools]

    def answer(self, question: str) -> AgentResult:
        messages: ResponseInputParam = [
            EasyInputMessageParam(role="system", content=self.instructions),
            EasyInputMessageParam(role="user", content=question)
        ]

        response: Response = self.client.responses.create(model=self.model, input=messages, tools=self.tool_params)

        while response.output_text == "":
            for tool_call in response.output:
                if not isinstance(tool_call, ResponseFunctionToolCall):
                    continue
                new_messages = self.invoke_tool(tool_call)
                messages.extend(new_messages)

            response = self.client.responses.create(model=self.model, input=messages, tools=self.tool_params)

        tool_calls = [
            ToolCall(name=message["name"], arguments=json.loads(message["arguments"]))
            for message in messages if "type" in message and message["type"] == "function_call"
        ]

        return AgentResult(response=response.output_text, tool_calls=tool_calls)

    def invoke_tool(self, tool_call: ResponseFunctionToolCall) -> ResponseInputParam:
        arguments = json.loads(tool_call.arguments)
        logger.debug(f"calling %s with args %s", tool_call.name, arguments)
        tool = next((tool for tool in self.tools if tool.name == tool_call.name), None)
        if tool is None:
            raise Exception(f"No tool found with name {tool_call.name}")

        return [
            ResponseFunctionToolCallParam(
                id=tool_call.id,
                arguments=tool_call.arguments,
                call_id=tool_call.call_id,
                name=tool_call.name,
                type="function_call",
            ),
            FunctionCallOutput(
                call_id=tool_call.call_id,
                output=tool.invoke(**arguments),
                type="function_call_output",
            )
        ]
