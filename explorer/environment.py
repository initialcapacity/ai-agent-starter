import os
from dataclasses import dataclass


@dataclass
class Environment:
    open_ai_key: str
    github_token: str

    @classmethod
    def from_env(cls) -> 'Environment':
        return cls(
            open_ai_key=require_env('OPEN_AI_KEY'),
            github_token=require_env('GITHUB_TOKEN'),
        )

def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise Exception(f'Unable to read {name} from the environment')
    return value
