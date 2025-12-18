import matplotlib.pyplot as plt

from core.github_client import GitHubClient
from core.metrics.timeline import TimelineMetric


def plot_timeline(username: str, output_dir="reports") -> str:
    client = GitHubClient()
    metric = TimelineMetric(client, username)

    data = metric.yearly_average_gap()
    years = sorted(data.keys())
    values = [data[y] for y in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, values, marker="o")
    plt.title("Evolução da Regularidade de Commits ao Longo dos Anos")
    plt.xlabel("Ano")
    plt.ylabel("Média de dias entre commits")
    plt.grid(True)

    path = f"{output_dir}/timeline_consistency.png"
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path
