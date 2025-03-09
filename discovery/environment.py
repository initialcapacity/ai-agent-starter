import os
from dataclasses import dataclass


@dataclass
class Environment:
    open_ai_key: str
    root_log_level: str
    discovery_log_level: str
    use_flask_debug_mode: bool
    port: str
    flask_secret_key: str

    github_oauth_enabled: bool
    github_client_id: str
    github_client_secret: str
    allowed_domains: str
    allowed_addresses: str

    @classmethod
    def from_env(cls) -> 'Environment':
        enable_oauth = os.environ.get('GITHUB_OAUTH_ENABLED', 'false') == 'true'

        return cls(
            open_ai_key=require_env('OPEN_AI_KEY'),
            root_log_level=os.environ.get('ROOT_LOG_LEVEL', 'INFO'),
            discovery_log_level=os.environ.get('DISCOVERY_LOG_LEVEL', 'INFO'),
            use_flask_debug_mode=os.environ.get('USE_FLASK_DEBUG_MODE', 'false') == 'true',
            port=os.environ.get('PORT', '5050'),
            flask_secret_key=require_env('FLASK_SECRET_KEY'),
            github_oauth_enabled=enable_oauth,
            github_client_id=require_env('GITHUB_CLIENT_ID') if enable_oauth else '',
            github_client_secret=require_env('GITHUB_CLIENT_SECRET') if enable_oauth else '',
            allowed_domains=os.environ.get('ALLOWED_DOMAINS', ""),
            allowed_addresses=os.environ.get('ALLOWED_ADDRESSES', ""),
        )

def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise Exception(f'Unable to read {name} from the environment')
    return value
