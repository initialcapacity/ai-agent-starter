import random


class LocalRepoClient(object):
    def is_repositories_checked_out(self, repository_api_url: str) -> bool:
        # return bool(random.getrandbits(1))
        return False

    def check_out_repositories(self, repository_api_url: str):
        # no-op
        pass