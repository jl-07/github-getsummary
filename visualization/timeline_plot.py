import matplotlib.pyplot as plt
from typing import Dict

from core.github_client import GitHubClient
from core.metrics.timeline import TimelineMetric



class TimelinePlot:
    def __init__(self, data: Dict[int, float]) -> None:
        self.data = data

    def plot(self, output_path: str) -> None:
        if not self.data:
            return

        years = sorted(self.data.keys())
        values = [self.data[y] for y in years]

        plt.figure(figsize=(10, 5))
        plt.plot(years, values, marker="o")
        plt.title("Evolução da Regularidade de Commits ao Longo dos Anos")
        plt.xlabel("Ano")
        plt.ylabel("Média de dias entre commits")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()


def plot_timeline(username: str, output_dir="reports") -> str:
    client = GitHubClient()
    metric = TimelineMetric(client, username)
    data = metric.yearly_average_gap()

    path = f"{output_dir}/timeline_consistency.png"
    
    plotter = TimelinePlot(data)
    plotter.plot(path)

    return path
