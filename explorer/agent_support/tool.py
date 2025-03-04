from dataclasses import dataclass
from typing import Callable, List
from inspect import signature, Parameter


@dataclass
class Argument:
    name: str
    type: str
    required: bool


@dataclass
class Tool:
    name: str
    description: str
    action: Callable
    arguments: List[Argument]

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        argument.name: {"type": argument.type}
                        for argument in self.arguments
                    },
                    "required": [argument.name for argument in self.arguments if argument.required],
                }
            }
        }


def json_type(parameter: Parameter) -> str:
    type_name = parameter.annotation.__name__
    if type_name == "str":
        return "string"
    elif type_name == "int" or type_name == "float":
        return "number"
    elif type_name == "bool":
        return "boolean"
    elif type_name == "_empty":
        raise Exception(f"Type annotation missing for tool parameter '{parameter.name}'")
    else:
        raise Exception(f"Unsupported argument type '{type_name}' for tool parameter '{parameter.name}'")


def argument_from_parameter(parameter: Parameter) -> Argument:
    return Argument(
        name=parameter.name,
        type=json_type(parameter),
        required=parameter.default == Parameter.empty
    )


def tool() -> Callable[[Callable], Tool]:
    def wrapper(action: Callable) -> Tool:
        return_type = signature(action).return_annotation.__name__
        if return_type != 'str':
            raise Exception(f"Unsupported return type: {return_type}")

        parameters = signature(action).parameters.values()
        return Tool(
            name=action.__name__,
            description=action.__doc__,
            action=action,
            arguments=[argument_from_parameter(parameter) for parameter in parameters]
        )

    return wrapper
