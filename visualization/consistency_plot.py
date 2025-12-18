import matplotlib.pyplot as plt
from typing import List
from pathlib import Path

from core.github_client import GitHubClient
from core.metrics.consistency import ConsistencyMetric


def plot_commit_gaps(username: str, output_dir: str = "reports") -> Path:
    client = GitHubClient()
    metric = ConsistencyMetric(client, username)

    gaps: List[int] = []

    repos = client.iter_user_repositories(username)
    for repo in repos:
        dates = metric._commit_dates(repo.full_name)
        dates = sorted(dates)

        for i in range(1, len(dates)):
            gaps.append((dates[i] - dates[i - 1]).days)

    if not gaps:
        raise RuntimeError("Nenhum dado suficiente para gerar gráfico.")

    # 📁 cria pasta de saída
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    image_path = output_path / "commit_gap_distribution.png"

    plt.figure(figsize=(10, 5))
    plt.hist(gaps, bins=20)
    plt.title("Distribuição dos Intervalos entre Commits (dias)")
    plt.xlabel("Dias entre commits")
    plt.ylabel("Frequência")

    plt.tight_layout()
    plt.savefig(image_path)   # 🔹 salva imagem
    plt.close()               # 🔹 fecha figura (boa prática)

    return image_path
