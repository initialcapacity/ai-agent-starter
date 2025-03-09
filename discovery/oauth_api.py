import logging

from flask import Blueprint, redirect, request, g, render_template
from flask.typing import ResponseReturnValue

from discovery.auth.allowed_emails import AllowedEmails
from discovery.auth.requre_authentication import require_authentication
from discovery.auth.session_manager import SessionManager
from discovery.github_support.github_oauth_client import GithubOAuthClient

logger = logging.getLogger(__name__)


def oauth_api(
        oauth_client: GithubOAuthClient,
        allowed_email_addresses: AllowedEmails,
) -> Blueprint:
    api = Blueprint('oauth_api', __name__)

    @api.get('/login')
    def login_page() -> ResponseReturnValue:
        return render_template('oauth_login.html', auth_url=oauth_client.auth_url())

    @api.get('/logout')
    @require_authentication
    def log_out() -> ResponseReturnValue:
        logger.info(f"Logging out user %s", g.username)
        SessionManager.logout()
        return redirect("/login")

    @api.get('/oauth/callback')
    def callback() -> ResponseReturnValue:
        access_token = oauth_client.fetch_access_token(request.args['code'])
        if access_token is None:
            logger.error('no access token found')
            return redirect('/')

        user_info = oauth_client.read_user_info_from_token(access_token)
        if user_info is None:
            logger.error("user info not found on token")
            return redirect("/")
        if not allowed_email_addresses.include(*user_info.emails):
            logger.error("none of the email addresses  for user '%s' are allowed: %s", user_info.username,
                         user_info.emails)
            return redirect("/")

        SessionManager.login(user_info.username, access_token)
        return redirect("/")

    return api
