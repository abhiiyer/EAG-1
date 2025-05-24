# report_generator.py
import json
from datetime import datetime

def load_log(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def format_line(text):
    return f"{text}\n"

def generate_summary():
    plan_log = load_log("./logs/plan_execution.log")
    step_history = load_log("./logs/step_history.log")
    transitions = load_log("./logs/strategy_transitions.log")

    summary_txt = ""
    summary_txt += format_line("📋 === EXECUTION DIAGNOSTIC SUMMARY ===")

    # Step Summary
    total_steps = len(step_history)
    successful_steps = sum(
        1 for entries in step_history.values() if any(e["status"] == "Success" for e in entries)
    )
    failed_steps = total_steps - successful_steps

    summary_txt += format_line(f"\n🧠 Total Steps Executed: {total_steps}")
    summary_txt += format_line(f"✅ Successful Steps: {successful_steps}")
    summary_txt += format_line(f"❌ Failed Steps: {failed_steps}")

    # What failed
    summary_txt += format_line("\n❗ Steps That Failed:")
    for step, entries in step_history.items():
        if not any(e["status"] == "Success" for e in entries):
            summary_txt += format_line(f" - {step} → {entries[-1]['status']}")

    # Strategy Transitions
    summary_txt += format_line("\n🔄 Strategy Transitions:")
    if transitions:
        for t in transitions:
            summary_txt += format_line(
                f" → {t['from_strategy']} → {t['to_strategy']} | Reason: {t['reason']}"
            )
    else:
        summary_txt += format_line("No strategy transitions occurred.")

    # Plan Execution Log
    summary_txt += format_line("\n📦 Step Execution Log:")
    if plan_log:
        for log in plan_log[-5:]:
            step = log['step']
            status = log['status']
            timestamp = log['timestamp']
            summary_txt += format_line(f" - {step} [{status}] @ {timestamp}")
    else:
        summary_txt += format_line("No plan executions logged.")

    summary_txt += format_line("\n✅ Diagnostic summary generated.\n")

    print(summary_txt)
    
    # 🔄 Add timestamp suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"final_diagnostic_report_{timestamp}.txt"
    html_filename = f"final_diagnostic_report_{timestamp}.html"

    # Save to plain text file
    with open("final_diagnostic_report.txt", "w", encoding="utf-8") as f:
        f.write(summary_txt)

    # Save to HTML
    html_content = summary_txt.replace("\n", "<br>")
    html_wrapper = f"""<html><body style='font-family:Arial;'>
    <h2>Execution Diagnostic Summary</h2><p>{html_content}</p></body></html>"""

    with open("final_diagnostic_report.html", "w", encoding="utf-8") as f:
        f.write(html_wrapper)

    print(f"📁 Saved to: {txt_filename} and {html_filename}")

    #print("📁 Saved to: final_diagnostic_report.txt and final_diagnostic_report.html")

if __name__ == "__main__":
    generate_summary()
