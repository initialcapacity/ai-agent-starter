import logging
import json
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urlencode

import requests
from requests.auth import HTTPBasicAuth

from discovery.github_support.github_client import GithubClient

logger = logging.getLogger(__name__)


@dataclass
class GithubUserInfo:
    username: str
    emails: List[str]


class GithubOAuthClient:
    def __init__(self, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret

    def auth_url(self) -> str:
        query_string = urlencode({
            'client_id': self.__client_id,
            'scope': 'read:user,user:email,repo',
        })
        return f"https://github.com/login/oauth/authorize?{query_string}"

    def fetch_access_token(self, code: str) -> Optional[str]:
        response = requests.post(f'https://github.com/login/oauth/access_token', data={
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'code': code,
        }, headers={'Accept': 'application/json'})

        if response.status_code != 200:
            return None

        return response.json().get('access_token')

    def read_user_info_from_token(self, token: str) -> Optional[GithubUserInfo]:
        response = requests.post(
            f"https://api.github.com/applications/{self.__client_id}/token",
            headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
            auth=HTTPBasicAuth(self.__client_id, self.__client_secret),
            data=json.dumps({"access_token": token}),
        )

        if response.status_code != 200:
            logger.error(f"Failed to read user info from token: %s", response.text)
            return None

        body = response.json()
        if "user" not in body or ("login" not in body["user"]):
            logger.error(f"Failed to decode user info from token: %s", response.text)
            return None

        emails = GithubClient(access_token=token).get_emails()
        if len(emails) == 0:
            logger.error(f"Failed to read emails for token")
            return None

        return GithubUserInfo(
            username=body["user"]["login"],
            emails=emails,
        )
