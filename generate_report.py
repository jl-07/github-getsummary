from pathlib import Path

from core.github_client import GitHubClient
from core.metrics.consistency import ConsistencyMetric
from visualization.consistency_plot import plot_commit_gaps

USERNAME = "octocat"

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

client = GitHubClient()
metric = ConsistencyMetric(client, USERNAME)

avg = metric.average_gap_days()
var = metric.gap_variance()
image_path = plot_commit_gaps(USERNAME, output_dir="reports")

report = f"""
# 📊 Relatório de Consistência de Commits

**Usuário analisado:** `{USERNAME}`

## 📈 Métricas
- **Média de dias entre commits:** {avg}
- **Variância dos intervalos:** {var}

## 🖼️ Visualização
![Distribuição dos intervalos entre commits]({image_path.name})

## 🔍 Interpretação
- Média baixa indica frequência de commits
- Variância alta indica ciclos de atividade e pausa
"""

report_path = REPORTS_DIR / "consistency_report.md"
report_path.write_text(report.strip(), encoding="utf-8")

print("Relatório gerado em:", report_path)
