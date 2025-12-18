print("TESTE CONSISTENCY RODANDO")

from core.github_client import GitHubClient
from core.metrics.consistency import ConsistencyMetric

client = GitHubClient()
metric = ConsistencyMetric(client, "jl-07")

print("Média:", metric.average_gap_days())
print("Variância:", metric.gap_variance())
print("CV:", metric.coefficient_of_variation())
