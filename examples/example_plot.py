from visualization.consistency_plot import plot_commit_gaps

print("Generating plot for octocat...")
image = plot_commit_gaps("octocat")
print("Gráfico salvo em:", image)
