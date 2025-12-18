from __future__ import annotations
import json
import os
from typing import Literal

from core.github_client import GitHubClient, Repository
from core.metrics.consistency import ConsistencyMetric
from core.metrics.timeline import TimelineMetric
from visualization.consistency_plot import ConsistencyPlot
from visualization.timeline_plot import TimelinePlot

def analyze_repositories(
    client: GitHubClient,
    repos: list[Repository],
    output_path: str | None = None,
    fmt: Literal["md", "html", "json"] = "md",
) -> str:
    # Consistency Metrics
    cons_metric = ConsistencyMetric(client, repositories=repos)
    gaps = cons_metric._commit_gaps()
    mean_gap = cons_metric.average_gap_days()
    variance_gap = cons_metric.gap_variance()

    # Timeline Metrics
    time_metric = TimelineMetric(client, repositories=repos)
    timeline_data = time_metric.yearly_average_gap()

    metrics = {
        "mean_gap_days": mean_gap,
        "variance_gap_days": variance_gap,
        "total_repos": len(repos),
    }

    if fmt == "json":
        result = json.dumps(metrics, indent=2)
        if output_path:
            with open(output_path, "w") as f:
                f.write(result)
        return result

    # Generate Plots
    reports_dir = os.path.dirname(output_path) if output_path else "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Plot Consistency
    if gaps:
        plot_cons = ConsistencyPlot(gaps)
        plot_cons.plot(os.path.join(reports_dir, "consistency.png"))
    
    # Plot Timeline
    if timeline_data:
        plot_time = TimelinePlot(timeline_data)
        plot_time.plot(os.path.join(reports_dir, "timeline.png"))

    # Generate Text Report
    if fmt == "html":
        content = f"""
        <html>
        <body>
            <h1>Career Telemetry</h1>
            <p>Repos: {len(repos)}</p>
            <p>Mean Gap: {metrics['mean_gap_days']:.2f} days</p>
            <p>Variance: {metrics['variance_gap_days']:.2f}</p>
            <img src="consistency.png" />
            <img src="timeline.png" />
        </body>
        </html>
        """
    else:
        content = f"""
# Career Telemetry Report

- Repositories Analyzed: {len(repos)}
- Mean Gap: {metrics['mean_gap_days']:.2f} days
- Variance: {metrics['variance_gap_days']:.2f}

![Consistency](consistency.png)
![Timeline](timeline.png)
        """

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    return content
