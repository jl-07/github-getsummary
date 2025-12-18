import matplotlib.pyplot as plt
from typing import List
from pathlib import Path

from core.github_client import GitHubClient
from core.metrics.consistency import ConsistencyMetric


class ConsistencyPlot:
    def __init__(self, gaps: List[int]) -> None:
        self.gaps = gaps

    def plot(self, output_path: str) -> None:
        if not self.gaps:
            return

        plt.figure(figsize=(10, 5))
        plt.hist(self.gaps, bins=20)
        plt.title("Distribuição dos Intervalos entre Commits (dias)")
        plt.xlabel("Dias entre commits")
        plt.ylabel("Frequência")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()


def plot_commit_gaps(username: str, output_dir: str = "reports") -> Path:
    client = GitHubClient()
    metric = ConsistencyMetric(client, username)
    gaps = metric._commit_gaps()

    if not gaps:
        raise RuntimeError("Nenhum dado suficiente para gerar gráfico.")

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    image_path = output_path / "commit_gap_distribution.png"
    
    plotter = ConsistencyPlot(gaps)
    plotter.plot(str(image_path))

    return image_path
