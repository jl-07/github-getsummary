import time
import json
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch
from core.github_client import GitHubClient

@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_cache_miss_writes_to_disk(temp_cache_dir):
    with patch("requests.Session.get") as mock_get:
        # Setup Mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "fresh"}
        mock_response.headers = {"ETag": "123", "X-RateLimit-Remaining": "10"}
        mock_get.return_value = mock_response

        client = GitHubClient(token="abc", cache_dir=temp_cache_dir)
        data = client._request("https://api.github.com/test")

        # Verify returned data
        assert data == {"data": "fresh"}
        
        # Verify cache file created
        # We don't know the hash exactly without re-hashing, so check directory list
        files = os.listdir(temp_cache_dir)
        assert len(files) == 1
        
        # Verify content
        with open(os.path.join(temp_cache_dir, files[0]), "r") as f:
            cached = json.load(f)
            assert cached["data"] == {"data": "fresh"}
            assert cached["headers"]["ETag"] == "123"

def test_cache_hit_fresh_no_request(temp_cache_dir):
    with patch("requests.Session.get") as mock_get:
        client = GitHubClient(token="abc", cache_dir=temp_cache_dir, ttl_seconds=3600)
        
        # Seed Cache
        import hashlib
        url = "https://api.github.com/test"
        hashed = hashlib.md5(url.encode("utf-8")).hexdigest()
        cache_path = os.path.join(temp_cache_dir, f"{hashed}.json")
        
        with open(cache_path, "w") as f:
            json.dump({
                "timestamp": time.time(), # Now
                "headers": {"ETag": "123"},
                "data": {"data": "cached"}
            }, f)

        # Call
        data = client._request(url)

        # Verify
        assert data == {"data": "cached"}
        mock_get.assert_not_called()

def test_cache_hit_stale_returns_304(temp_cache_dir):
    with patch("requests.Session.get") as mock_get:
        client = GitHubClient(
            token="abc", cache_dir=temp_cache_dir, ttl_seconds=1
        )  # Short TTL
        
        # Seed Stale Cache
        import hashlib
        url = "https://api.github.com/test"
        hashed = hashlib.md5(url.encode("utf-8")).hexdigest()
        cache_path = os.path.join(temp_cache_dir, f"{hashed}.json")
        
        start_time = time.time() - 100
        with open(cache_path, "w") as f:
            json.dump({
                "timestamp": start_time,
                "headers": {"ETag": "123"},
                "data": {"data": "old"}
            }, f)

        # Setup Mock 304
        mock_response = MagicMock()
        mock_response.status_code = 304
        mock_response.headers = {"X-RateLimit-Remaining": "10"}
        mock_get.return_value = mock_response

        # Call
        data = client._request(url)

        # Verify
        assert data == {"data": "old"}
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["headers"]["If-None-Match"] == "123"
        
        # Verify timestamp updated
        with open(cache_path, "r") as f:
            cached = json.load(f)
            assert cached["timestamp"] > start_time

def test_cache_does_not_save_errors(temp_cache_dir):
    with patch("requests.Session.get") as mock_get:
        client = GitHubClient(token="abc", cache_dir=temp_cache_dir)
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        # Expect Exception
        from core.github_client import GitHubAPIError
        with pytest.raises(GitHubAPIError):
            client._request("https://api.github.com/bad")
            
        # Verify no cache
        assert len(os.listdir(temp_cache_dir)) == 0
