
from rich.console import Console
from rich.panel import Panel
from datetime import datetime, timedelta
from fpdf import FPDF

console = Console()

def summarize_customer(data: dict) -> str:
    summary = f"""👤 {data.get("name", "[Unknown]")}
🏢 Employer: {data.get("employer", "N/A")} | Industry: {data.get("industry", "N/A")}
💰 Max Net Worth: AED {max(data.get("net_worth_history", []))}
📊 Balance Trend: {data['balance_trend']}
🧾 Recent Activity: {data.get("recent_activity", "No major activity.")}
📦 Products: {", ".join(data['products'])}
📣 Campaign History: {data.get("campaign_history", "None")}"""
    console.print(Panel(summary, title="Customer Profile", border_style="cyan"))
    return summary

def customer_type(data: dict) -> str:
    if data["balance_trend"] == "drop" and "Wio Bank" in data["recent_activity"]:
        return "📉 At Risk"
    elif data["balance_trend"] == "stable":
        return "🧍 Passive Saver"
    elif data["balance_trend"] == "increase" and "Fixed Deposit" in data["products"]:
        return "💼 Premium Growth"
    elif "Credit Card" in data["products"]:
        return "🎯 Spender"
    return "🧠 Unclassified"

def recommend_nba(data: dict) -> str:
    if data['balance_trend'] == "drop":
        action = "⚠️ Balance dropped; recommend FD renewal or FX offer."
    elif data['balance_trend'] == "increase":
        action = "📈 Balances increasing; explore investment or premium upsell."
    else:
        action = "📊 Stable balance; maintain engagement and suggest credit cards."
    console.print(Panel(action, title="Next Best Action", border_style="magenta"))
    return action

def engagement_score(data: dict) -> int:
    score = 50
    if "Fixed Deposit" in data["products"]:
        score += 15
    if data["balance_trend"] == "drop":
        score -= 25
    if "Wio Bank" in data["recent_activity"]:
        score -= 10
    if "Credit Card" in data["products"]:
        score += 10
    return max(min(score, 100), 0)

def show_engagement(data: dict):
    score = engagement_score(data)
    label = "⚠️ At Risk" if score < 60 else "✅ Stable"
    result = f"{score}/100 - {label}"
    console.print(Panel(result, title="Engagement Score", border_style="red" if score < 60 else "green"))
    return result

def show_balance_chart(balance_history: dict):
    console.print(Panel("📊 Last 3-Months Balance Trend", border_style="blue"))
    for month, value in balance_history.items():
        bars = "█" * max(1, int(value / 10000))
        print(f"{month}: {bars:<15} (AED {value})")

def generate_scripts(data: dict) -> str:
    name = data.get("name", "Customer")
    subject = f"Let’s optimize your finances, {name}" if data["balance_trend"] == "drop" else f"Thank you for banking with us, {name}"
    employer = data.get("employer", "your organization")
    call_script = f"Hi {name}, I noticed your recent transactions. As an employee at {employer}, we’d love to offer a 4.25% FD tailored to your needs."
    email = f"""Subject: {subject}

Hi {name},

I observed your recent activity and believe we can help optimize your savings through fixed deposits or FX plans.
Since you’re with {employer}, we have special options available including an FD at 4.25% p.a.

Would you like to explore this?

Best,
Your RM"""
    combined = f"CALL SCRIPT:\n{call_script}\n\nEMAIL DRAFT:\n{email}"
    console.print(Panel(combined, title="Generated Scripts", border_style="green"))
    return combined

def rm_todo_list():
    checklist = """✔ Review customer in CRM
✔ Offer relevant FD/FX pitch
✔ Call before EOD
✔ Schedule follow-up in 3 days
✔ Mark customer as 'At Risk' if applicable"""
    console.print(Panel(checklist, title="📋 RM To-Do", border_style="yellow"))

def get_follow_up_date():
    d = datetime.today()
    while d.weekday() >= 5:
        d += timedelta(days=1)
    d += timedelta(days=3)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d.strftime('%A, %b %d, %Y')

def generate_pdf_summary(customer, nba, score, ctype, follow_up):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    lines = [
        f"Customer Summary Report - {customer['name']}",
        f"Employer: {customer['employer']} | Industry: {customer['industry']}",
        f"Net Worth Peak: AED {max(customer['net_worth_history'])}",
        f"Risk Score: {score}/100",
        f"Customer Type: {ctype}",
        f"Next Best Action: {nba}",
        f"Suggested Follow-up Date: {follow_up}",
        "",
        "Recent Activity: " + customer["recent_activity"],
        "Balance Trend: " + customer["balance_trend"],
        "Products: " + ", ".join(customer["products"])
    ]
    for line in lines:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(f"report_{customer['name']}.pdf")
    console.print(f"[green]📄 PDF summary generated: report_{customer['name']}.pdf[/green]")

def show_analytics(customers):
    from collections import Counter
    from rich.table import Table
    from statistics import mean

    console.print("\n📊 [bold]Customer Segment Analytics[/bold]")
    
    scores = [engagement_score(c) for c in customers]
    avg_score = mean(scores)

    types = [customer_type(c) for c in customers]
    type_count = Counter(types)

    table = Table(title="Customer Type Distribution")
    table.add_column("Type", justify="left")
    table.add_column("Count", justify="right")
    for t, count in type_count.items():
        table.add_row(t, str(count))
    
    console.print(table)
    console.print(f"📈 Average Engagement Score: [bold blue]{avg_score:.1f}[/bold blue]/100")
