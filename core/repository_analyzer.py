from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Dict, List

from core.github_client import Repository


@dataclass(frozen=True)
class RepositorySnapshot:
    year: int
    total_repos: int
    avg_size_kb: float
    languages: Dict[str, int]


class RepositoryAnalyzer:
    def __init__(self, repositories: Iterable[Repository]) -> None:
        self.repositories = list(repositories)

    def _filter_relevant(self) -> List[Repository]:
        """
        Remove forks and invalid repositories.
        """
        return [
            repo for repo in self.repositories
            if not repo.is_fork
        ]

    def group_by_year(self) -> Dict[int, List[Repository]]:
        grouped: Dict[int, List[Repository]] = defaultdict(list)

        for repo in self._filter_relevant():
            year = datetime.fromisoformat(
                repo.created_at.replace("Z", "")
            ).year
            grouped[year].append(repo)

        return dict(grouped)

    def yearly_snapshots(self) -> List[RepositorySnapshot]:
        snapshots: List[RepositorySnapshot] = []

        for year, repos in sorted(self.group_by_year().items()):
            total_size = sum(r.size_kb for r in repos)
            avg_size = total_size / len(repos)

            languages: Dict[str, int] = defaultdict(int)
            for repo in repos:
                if repo.language:
                    languages[repo.language] += 1

            snapshots.append(
                RepositorySnapshot(
                    year=year,
                    total_repos=len(repos),
                    avg_size_kb=round(avg_size, 2),
                    languages=dict(languages),
                )
            )

        return snapshots
