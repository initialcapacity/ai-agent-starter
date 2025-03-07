import logging

from discovery.app import create_app
from discovery.environment import Environment

env = Environment.from_env()
logging.basicConfig(level=env.root_log_level)
logging.getLogger('discovery').setLevel(level=env.discovery_log_level)

if __name__ == '__main__':
    create_app().run(debug=env.use_flask_debug_mode, host="0.0.0.0", port=env.port)
