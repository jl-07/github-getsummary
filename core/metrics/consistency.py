from datetime import datetime
from statistics import mean, stdev
from typing import List

from core.github_client import GitHubClient, Repository


class ConsistencyMetric:
    """
    Measures how consistent a developer's commit activity is over time.
    """

    def __init__(
        self,
        client: GitHubClient,
        username: str | None = None,
        repositories: List[Repository] | None = None,
    ) -> None:
        self.client = client
        self.username = username
        self.repositories = repositories

    def _commit_dates(self, repo_full_name: str) -> List[datetime]:
        try:
            commits = self.client._request(
                f"https://api.github.com/repos/{repo_full_name}/commits",
                params={"per_page": 100},
            )
        except Exception:
            return []

        dates: List[datetime] = []
        if not commits or not isinstance(commits, list):
            return dates
            
        for commit in commits:
            if "commit" in commit:
                date_str = commit["commit"]["author"]["date"]
                dates.append(datetime.fromisoformat(date_str.replace("Z", "")))

        return dates

    def _commit_gaps(self) -> List[int]:
        gaps: List[int] = []

        if self.repositories:
            repos = self.repositories
        elif self.username:
            repos = list(self.client.iter_user_repositories(self.username))
        else:
            return []

        for repo in repos:
            dates = sorted(self._commit_dates(repo.full_name))
            for i in range(1, len(dates)):
                gaps.append((dates[i] - dates[i - 1]).days)

        return gaps

    def average_gap_days(self) -> float:
        gaps = self._commit_gaps()
        if not gaps:
            return 0.0
        return round(mean(gaps), 2)

    def gap_variance(self) -> float:
        gaps = self._commit_gaps()
        if len(gaps) < 2:
            return 0.0
        return round(stdev(gaps), 2)

    def coefficient_of_variation(self) -> float:
        gaps = self._commit_gaps()

        if len(gaps) < 2:
            return 0.0

        avg = mean(gaps)
        if avg == 0:
            return 0.0

        return round(stdev(gaps) / avg, 2)
