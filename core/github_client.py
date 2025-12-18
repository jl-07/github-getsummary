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
    def __init__(
        self,
        token: Optional[str] = None,
        cache_dir: str = ".cache",
        ttl_seconds: int = 43200,  # 12 hours
    ) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        self.session = requests.Session()

        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

        self.session.headers.update({"Accept": "application/vnd.github+json"})

        if self.cache_dir:
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, url: str, params: dict | None = None) -> str:
        import hashlib
        import json

        # Create a unique key for URL + params
        key = url
        if params:
            key += json.dumps(params, sort_keys=True)
            
        hashed = hashlib.md5(key.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed}.json")

    def _read_cache(self, cache_path: str) -> dict | None:
        import json
        
        if not os.path.exists(cache_path):
            return None
            
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def _write_cache(self, cache_path: str, response: requests.Response) -> None:
        import json
        
        # Only cache successful GET requests
        if response.status_code != 200:
            return

        cache_data = {
            "timestamp": time.time(),
            "headers": dict(response.headers),
            "data": response.json(),
        }
        
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f)
        except OSError:
            pass

    def _handle_rate_limit(self, response: requests.Response) -> None:
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))

        if remaining <= 0:
            reset_timestamp = int(
                response.headers.get("X-RateLimit-Reset", time.time())
            )
            sleep_for = max(reset_timestamp - int(time.time()), 1)
            time.sleep(sleep_for)

    def _request(self, url: str, params: dict | None = None) -> dict:
        cache_path = self._get_cache_path(url, params)
        cached = self._read_cache(cache_path)
        request_headers = {}

        # Check Cache TTL
        if cached:
            age = time.time() - cached["timestamp"]
            if age < self.ttl_seconds:
                # Cache is fresh, return immediately
                return cached["data"]
            
            # Cache is stale, try conditional request
            if "ETag" in cached["headers"]:
                request_headers["If-None-Match"] = cached["headers"]["ETag"]
            if "Last-Modified" in cached["headers"]:
                request_headers["If-Modified-Since"] = cached["headers"][
                    "Last-Modified"
                ]

        # Make Request
        response = self.session.get(url, params=params, headers=request_headers)

        # Handle 304 Not Modified
        if response.status_code == 304 and cached:
            # Update timestamp to refresh TTL
            cached["timestamp"] = time.time()
            # Optionally update headers if provided in 304
            cached["headers"].update(dict(response.headers))
            
            try:
                import json
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(cached, f)
            except OSError:
                pass
                
            return cached["data"]

        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API error {response.status_code}: {response.text}"
            )

        self._handle_rate_limit(response)
        self._write_cache(cache_path, response)
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

    def iter_org_repositories(
        self, orga: str, per_page: int = 100
    ) -> Iterator[Repository]:
        page = 1

        while True:
            data = self._request(
                f"{GITHUB_API_URL}/orgs/{orga}/repos",
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
