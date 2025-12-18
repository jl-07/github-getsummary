from core.github_client import GitHubClient
from core.repository_analyzer import RepositoryAnalyzer

client = GitHubClient()
repos = list(client.iter_user_repositories("octocat"))

analyzer = RepositoryAnalyzer(repos)
snapshots = analyzer.yearly_snapshots()

for snap in snapshots:
    print(snap)
