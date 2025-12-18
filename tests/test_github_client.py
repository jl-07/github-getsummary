import os
from unittest.mock import patch
from core.github_client import GitHubClient

def test_github_client_headers_without_token():
    # Ensure no token in env
    with patch.dict(os.environ, {}, clear=True):
        client = GitHubClient(token=None)
        headers = client.session.headers
        assert "Authorization" not in headers
        assert headers["Accept"] == "application/vnd.github+json"

def test_github_client_headers_with_token():
    client = GitHubClient(token="fake-token")
    headers = client.session.headers
    assert headers["Authorization"] == "Bearer fake-token"
    assert headers["Accept"] == "application/vnd.github+json"
