import sys
import os
sys.path.append(os.getcwd())
from typer.testing import CliRunner  # noqa: E402
from unittest.mock import patch, MagicMock
from cli import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Git Career Telemetry CLI" in result.stdout

def test_cli_user_command_help():
    result = runner.invoke(app, ["user", "--help"])
    assert result.exit_code == 0
    assert "Analyze consistency for a specific GitHub user" in result.stdout

def test_cli_user_execution_mocked():
    with patch("core.github_client.GitHubClient.iter_user_repositories") as mock_iter, \
         patch("cli.analyze_repositories") as mock_analyze:
        
        # Mock Repos
        mock_repo = MagicMock()
        mock_iter.return_value = [mock_repo]
        
        # Mock Analysis Result
        mock_analyze.return_value = "Report Content"

        result = runner.invoke(app, ["user", "testuser", "--format", "json"])
        
        assert result.exit_code == 0
        assert "Found 1 repositories" in result.stdout
        assert "Report Content" in result.stdout

def test_cli_org_execution_mocked():
    with patch("core.github_client.GitHubClient.iter_org_repositories") as mock_iter:
        mock_iter.return_value = []
        result = runner.invoke(app, ["org", "testorg"])
        
        # Expect exit code 1 because no repos found
        assert result.exit_code == 1
        assert "No repositories found" in result.stdout
