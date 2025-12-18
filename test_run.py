from core.github_client import GitHubClient

client = GitHubClient()
repos = list(client.iter_user_repositories("octocat"))

print(f"Repos encontrados: {len(repos)}")
