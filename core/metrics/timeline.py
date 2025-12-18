from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Dict, List

from core.github_client import GitHubClient


class TimelineMetric:
    def __init__(self, client: GitHubClient, username: str) -> None:
        self.client = client
        self.username = username

    def yearly_average_gap(self) -> Dict[int, float]:
        gaps_by_year: Dict[int, List[int]] = defaultdict(list)

        repos = self.client.iter_user_repositories(self.username)

        for repo in repos:
            commits = self.client._request(
                f"https://api.github.com/repos/{repo.full_name}/commits",
                params={"per_page": 100},
            )

            dates = sorted(
                datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", ""))
                for c in commits
            )

            for i in range(1, len(dates)):
                year = dates[i].year
                gap = (dates[i] - dates[i - 1]).days
                gaps_by_year[year].append(gap)

        return {
            year: round(mean(gaps), 2)
            for year, gaps in gaps_by_year.items()
            if gaps
        }
