from flask import Blueprint, Flask
from flask.testing import FlaskClient


def test_client(blueprint: Blueprint, authenticated: bool = False) -> FlaskClient:
    app = Flask(__name__, template_folder='../discovery/templates')
    app.config['TESTING'] = True
    app.register_blueprint(blueprint)
    app.secret_key = 'test-secret'
    client = app.test_client()

    if authenticated:
        with client.session_transaction() as session:
            session["username"] = "some_user"
            session["github_token"] = "some_token"

    return client

