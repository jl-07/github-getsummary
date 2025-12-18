from pathlib import Path

from core.github_client import GitHubClient
from core.metrics.consistency import ConsistencyMetric

USERNAME = "octocat"  # depois trocamos para o seu

client = GitHubClient()
metric = ConsistencyMetric(client, USERNAME)

avg = metric.average_gap_days()
var = metric.gap_variance()

readme = f"""
# 🚀 Git Career Telemetry

Análise objetiva da minha evolução como desenvolvedor, baseada em **dados reais do GitHub**.

---

## 📊 Métrica de Consistência

- **Média de dias entre commits:** {avg}
- **Variância dos intervalos:** {var}

> Quanto menor a variância, mais consistente é a atividade ao longo do tempo.

---

## 📈 Distribuição dos intervalos entre commits

![Distribuição](reports/commit_gap_distribution.png)

---

## 🧭 Linha do tempo de consistência

![Timeline](reports/timeline_consistency.png)

---

## 🛠️ Stack

- Python
- GitHub REST API
- Matplotlib
- Análise temporal de dados

---

## 📌 Objetivo do projeto

Demonstrar evolução técnica real ao longo do tempo, indo além de contagem de commits.
"""

Path("README.md").write_text(readme.strip(), encoding="utf-8")

print("README.md gerado na raiz do projeto")
