from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Dict, List

from core.github_client import GitHubClient, Repository


class TimelineMetric:
    def __init__(
        self,
        client: GitHubClient,
        username: str | None = None,
        repositories: List[Repository] | None = None,
    ) -> None:
        self.client = client
        self.username = username
        self.repositories = repositories

    def yearly_average_gap(self) -> Dict[int, float]:
        gaps_by_year: Dict[int, List[int]] = defaultdict(list)

        if self.repositories:
            repos = self.repositories
        elif self.username:
            repos = list(self.client.iter_user_repositories(self.username))
        else:
            return {}

        for repo in repos:
            try:
                commits = self.client._request(
                    f"https://api.github.com/repos/{repo.full_name}/commits",
                    params={"per_page": 100},
                )
            except Exception:
                continue

            if not commits or not isinstance(commits, list):
                continue
                
            dates = []
            for c in commits:
                if "commit" in c:
                    dates.append(
                        datetime.fromisoformat(
                            c["commit"]["author"]["date"].replace("Z", "")
                        )
                    )
            
            dates.sort()

            for i in range(1, len(dates)):
                year = dates[i].year
                gap = (dates[i] - dates[i - 1]).days
                gaps_by_year[year].append(gap)

        return {
            year: round(mean(gaps), 2)
            for year, gaps in gaps_by_year.items()
            if gaps
        }
