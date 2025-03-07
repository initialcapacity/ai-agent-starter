import os
from dataclasses import dataclass


@dataclass
class Environment:
    open_ai_key: str
    github_token: str
    root_log_level: str
    discovery_log_level: str
    use_flask_debug_mode: bool
    port: str

    @classmethod
    def from_env(cls) -> 'Environment':
        return cls(
            open_ai_key=require_env('OPEN_AI_KEY'),
            github_token=require_env('GITHUB_TOKEN'),
            root_log_level=os.environ.get('ROOT_LOG_LEVEL', 'INFO'),
            discovery_log_level=os.environ.get('DISCOVERY_LOG_LEVEL', 'INFO'),
            use_flask_debug_mode=os.environ.get('USE_FLASK_DEBUG_MODE', 'false') == 'true',
            port=os.environ.get('PORT', '5050'),
        )

def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise Exception(f'Unable to read {name} from the environment')
    return value
