from pathlib import Path
import markdown

MD_PATH = Path("reports/consistency_report.md")
HTML_PATH = Path("reports/consistency_report.html")

md_text = MD_PATH.read_text(encoding="utf-8")

html_body = markdown.markdown(md_text, extensions=["extra"])

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Git Career Telemetry</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: auto;
            padding: 2rem;
            background: #f9f9f9;
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        img {{
            max-width: 100%;
            border: 1px solid #ddd;
            margin-top: 1rem;
        }}
        code {{
            background: #eee;
            padding: 2px 6px;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

HTML_PATH.write_text(html, encoding="utf-8")

print("HTML gerado em:", HTML_PATH)
