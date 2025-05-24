# dashboard_generator.py
import json
import webbrowser
from datetime import datetime

def load_log(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def generate_dashboard():
    step_history = load_log("./logs/step_history.log")
    tool_perf = load_log("./logs/tool_performance.log")
    transitions = load_log("./logs/strategy_transitions.log")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<html><head><title>Agent Dashboard</title>
    <style>
        body {{ font-family: Arial; padding: 20px; }}
        h2 {{ color: #2c3e50; }}
        .block {{ margin-bottom: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; }}
        th {{ background-color: #f0f0f0; }}
    </style>
    </head><body>
    <h2>🔍 Execution Dashboard</h2>
    <p>Generated at: {now}</p>
    <div class='block'>
        <h3>✅ Tool Performance</h3>
        <table>
        <tr><th>Tool</th><th>Success</th><th>Failure</th></tr>"""
    for tool, stats in tool_perf.items():
        html += f"<tr><td>{tool}</td><td>{stats['success']}</td><td>{stats['failure']}</td></tr>"
    html += "</table></div>"

    html += "<div class='block'><h3>🔄 Strategy Transitions</h3><ul>"
    if transitions:
        for t in transitions:
            html += f"<li>{t['timestamp']}: <b>{t['from_strategy']}</b> → <b>{t['to_strategy']}</b> — {t['reason']}</li>"
    else:
        html += "<li>No transitions logged.</li>"
    html += "</ul></div>"

    html += "<div class='block'><h3>📦 Step History</h3>"
    for step, entries in step_history.items():
        html += f"<b>{step}</b>: " + ", ".join([e['status'] for e in entries]) + "<br>"
    html += "</div>"

    html += "</body></html>"

    file = "agent_dashboard.html"
    with open(file, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(file)
    print(f"[✅] Dashboard generated and opened → {file}")

if __name__ == "__main__":
    generate_dashboard()
