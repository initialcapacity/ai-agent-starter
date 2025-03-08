import logging

from flask import Blueprint, render_template, request, Response, redirect, g
from flask.typing import ResponseReturnValue

from discovery.auth.requre_authentication import require_authentication
from discovery.auth.session_manager import SessionManager
from discovery.github_support.github_client import GithubClient

logger = logging.getLogger(__name__)


def authentication_page() -> Blueprint:
    page = Blueprint('authentication_page', __name__)

    @page.get('/login')
    def login_page() -> ResponseReturnValue:
        return render_template('login.html')

    @page.get('/logout')
    @require_authentication
    def log_out() -> ResponseReturnValue:
        logger.info(f"Logging out user %s", g.username)
        SessionManager.logout()
        return redirect("/login")

    @page.post('/login')
    def login_with_token() -> ResponseReturnValue:
        github_token = request.form.get('token')
        github_client = GithubClient(github_token)
        user = github_client.get_user()
        if user is None:
            logger.error(f"User not found")
            return Response("User not found", status=400)

        SessionManager.login(user.name, github_token)
        logger.info(f"Logged in user %s", user.name)

        return redirect("/")

    return page
