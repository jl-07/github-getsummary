# Git Career Telemetry

![CI](https://github.com/usuario/git-career-telemetry/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A tool to analyze **developer behavior and evolution** over time using public GitHub data. Instead of counting commits, it measures **regularity, consistency, and progression** via time-based metrics.

## ⚡ TL;DR
- **Analyze** consistency (mean gap, variance) for any user or organization.
- **Visualize** habits with timeline charts and histograms.
- **Cache-optimized** to respect GitHub API rate limits.

```bash
# Analyze a user
python cli.py user torvalds --format md

# Analyze an organization
python cli.py org facebook --top 10
```

---

## 🚀 Installation

### Option 1: Development Mode (Recommended)
```bash
git clone https://github.com/your-username/git-career-telemetry.git
cd git-career-telemetry
python -m venv venv
./venv/Scripts/activate  # Windows
# source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
```

### Option 2: Run "As Is"
Ensure you have Python 3.10+ installed.
```bash
pip install requests matplotlib typer
python cli.py --help
```

---

## 📖 Usage

### User Analysis
Checks consistency of a specific user across all their public repositories.
```bash
python cli.py user <username> [--ttl 12] [--format md|html|json] [--output report.html]
```

### Organization Analysis
Checks consistency of repositories belonging to an organization.
```bash
python cli.py org <orgname> --top 20
```

### Examples
See [examples/reports/](examples/reports/) for sample outputs.

---

## 🏗️ Architecture

The project is structured around Clean Architecture principles:

- **`core/`**: Business logic.
  - `github_client.py`: Handles API requests, rate limiting, and caching (ETag/304).
  - `metrics/`: Statistical calculations (Consistency, Timeline).
  - `use_cases.py`: Orchestrates fetching, calculation, and reporting.
- **`visualization/`**: Plotting logic using Matplotlib.
- **`cli.py`**: Entry point using Typer.

### Caching & Rate Limits
To avoid hitting GitHub's API rate limit (60 requests/hour unauthenticated):
- **Disk Cache**: Responses are stored in `.cache/` (hashed by URL + params).
- **Conditional Requests**: Uses `ETag` and `Last-Modified`.
  - If API returns **304 Not Modified**, the cached response is used (0 quota cost).
- **TTL**: Configurable (default 12h). Fresh cache hits don't even touch the network.

---

## 🔐 Security

- **Token Optional**: You can run without a token (lower rate limit).
- **Environment Variable**: To increase limits (5000 req/hour), set `GITHUB_TOKEN` in your environment or `.env` file (not committed).
- **No Sensitive Data**: The tool only reads public repository metadata.

---

## 🗺️ Roadmap

- [ ] Add support for GitLab/Bitbucket.
- [ ] Comparison mode (compare year X vs year Y).
- [ ] Export to PDF.
- [ ] Web UI (Streamlit/FastAPI).
- [ ] Activity Heatmap (like GitHub's profile graph).

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Open an Issue to discuss the change.
2. Fork the repository.
3. Create a branch (`feature/amazing-feature`).
4. Commit changes.
5. Open a Pull Request.

Ensure `pytest` and `ruff check .` pass before submitting.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.