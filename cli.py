import typer
from typing import Optional
from typing_extensions import Annotated

from core.github_client import GitHubClient
from core.use_cases import analyze_repositories

app = typer.Typer(help="Git Career Telemetry CLI")

@app.command()
def user(
    username: str,
    since: int = 180,
    fmt: Annotated[
        str, typer.Option("--format", help="Output format (md, html, json)")
    ] = "md",
    output: Optional[str] = typer.Option(None, help="Output file path"),
    ttl: int = typer.Option(12, help="Cache TTL in hours"),
):
    """
    Analyze consistency for a specific GitHub user.
    """
    client = GitHubClient(ttl_seconds=ttl * 3600)
    typer.echo(f"Fetching repositories for user: {username}...")
    repos = list(client.iter_user_repositories(username))
    
    if not repos:
        typer.echo("No repositories found.")
        raise typer.Exit(code=1)
        
    typer.echo(f"Found {len(repos)} repositories. Analyzing...")
    result = analyze_repositories(client, repos, output_path=output, fmt=fmt)
    
    if not output:
        typer.echo(result)
    else:
        typer.echo(f"Report saved to {output}")

@app.command()
def org(
    organization: str,
    top: int = typer.Option(None, help="Limit to top N repositories"),
    fmt: Annotated[str, typer.Option("--format")] = "md",
    output: Optional[str] = None,
    ttl: int = 12,
):
    """
    Analyze consistency for a GitHub organization.
    """
    client = GitHubClient(ttl_seconds=ttl * 3600)
    typer.echo(f"Fetching repositories for org: {organization}...")
    repos = list(client.iter_org_repositories(organization))
    
    if top:
        repos = repos[:top]
        
    if not repos:
        typer.echo("No repositories found.")
        raise typer.Exit(code=1)

    typer.echo(f"Found {len(repos)} repositories. Analyzing...")
    result = analyze_repositories(repos, output_path=output, fmt=fmt)

    if not output:
        typer.echo(result)
    else:
        typer.echo(f"Report saved to {output}")

if __name__ == "__main__":
    app()
