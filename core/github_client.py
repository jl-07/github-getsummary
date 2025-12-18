from __future__ import annotations

import os
import time
import requests
from dataclasses import dataclass
from typing import Iterator, Optional

GITHUB_API_URL = "https://api.github.com"


class GitHubAPIError(Exception):
    pass


@dataclass(frozen=True)
class Repository:
    name: str
    full_name: str
    is_fork: bool
    size_kb: int
    language: Optional[str]
    created_at: str
    updated_at: str


class GitHubClient:
    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.session = requests.Session()

        if self.token:
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json",
                }
            )



      

    def _handle_rate_limit(self, response: requests.Response) -> None:
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))

        if remaining <= 0:
            reset_timestamp = int(response.headers.get("X-RateLimit-Reset", time.time()))
            sleep_for = max(reset_timestamp - int(time.time()), 1)
            time.sleep(sleep_for)

    def _request(self, url: str, params: dict | None = None) -> dict:
        response = self.session.get(url, params=params)

        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API error {response.status_code}: {response.text}"
            )

        self._handle_rate_limit(response)
        return response.json()

    def iter_user_repositories(
        self, username: str, per_page: int = 100
    ) -> Iterator[Repository]:
        page = 1

        while True:
            data = self._request(
                f"{GITHUB_API_URL}/users/{username}/repos",
                params={
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated",
                },
            )

            if not data:
                break

            for repo in data:
                yield Repository(
                    name=repo["name"],
                    full_name=repo["full_name"],
                    is_fork=repo["fork"],
                    size_kb=repo["size"],
                    language=repo["language"],
                    created_at=repo["created_at"],
                    updated_at=repo["updated_at"],
                )

            page += 1
