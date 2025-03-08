from dataclasses import dataclass
from typing import Optional

from flask import session


@dataclass
class SessionUser:
    username: str
    github_token: str


class SessionManager:
    @staticmethod
    def login(username: str, github_token: str):
        session["username"] = username
        session["github_token"] = github_token

    @staticmethod
    def user() -> Optional[SessionUser]:
        if "username" not in session or "github_token" not in session:
            return None

        return SessionUser(
            username=session["username"],
            github_token=session["github_token"],
        )

    @staticmethod
    def logout():
        session.clear()
