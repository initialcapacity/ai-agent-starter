from functools import wraps

from flask import redirect, g

from discovery.auth.session_manager import SessionManager


def require_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = SessionManager.user()
        if user is None:
            return redirect("/login")

        g.username = user.username
        g.github_token = user.github_token
        return func(*args, **kwargs)

    return wrapper
