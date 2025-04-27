
import json
import csv
import os
from rich.console import Console
from rich.panel import Panel
from rm_tools import (
    summarize_customer, recommend_nba, show_engagement, generate_scripts,
    show_balance_chart, rm_todo_list, engagement_score, customer_type,
    get_follow_up_date, generate_pdf_summary,show_analytics
)

console = Console()

def suggest_customer(customers):
    scored = [(cust["name"], engagement_score(cust)) for cust in customers]
    scored.sort(key=lambda x: x[1])
    name, score = scored[0]
    return f"🔍 You should prioritize: [bold red]{name}[/bold red] (Risk Score: {score}/100)"

def display_customer_list(customers):
    show_analytics(customers)
    console.print(Panel("🔸 Select a customer to view:", border_style="cyan"))
    for idx, cust in enumerate(customers, 1):
        print(f"{idx}. {cust['name']}")
    print()

def save_to_csv(customer, nba, score, ctype, follow_up):
    filename = "rm_summary_log.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Employer", "Industry", "Risk Score", "Customer Type", "NBA", "Follow-up Date"])
        writer.writerow([customer["name"], customer["employer"], customer["industry"], score, ctype, nba, follow_up])
    console.print(f"[green]Customer summary saved to {filename}[/green]")

def main():
    console.print("[green]Launching RM Assist Ultimate Edition...[/green]")
    with open("customers.json", "r") as f:
        customers = json.load(f)

    while True:
        console.print(Panel("RM Assist – RM Intelligence Console", border_style="cyan"))
        console.print(suggest_customer(customers))

        display_customer_list(customers)

        choice = int(input("Enter customer number (1 - {}): ".format(len(customers))))
        selected = customers[choice - 1]

        console.print(Panel(f"You selected: {selected['name']}", border_style="blue"))
        score = engagement_score(selected)
        ctype = customer_type(selected)
        show_engagement(selected)
        show_balance_chart(selected["balance_history"])
        summarize_customer(selected)
        nba = recommend_nba(selected)
        generate_scripts(selected)
        rm_todo_list()

        follow_up = get_follow_up_date()
        print(f"📅 Suggested Follow-up: {follow_up}")

        export = input("💾 Save this summary to CSV? (Y/N): ").strip().lower()
        if export == 'y':
            save_to_csv(selected, nba, score, ctype, follow_up)

        pdf_opt = input("🖨️ Generate PDF summary report? (Y/N): ").strip().lower()
        if pdf_opt == 'y':
            generate_pdf_summary(selected, nba, score, ctype, follow_up)

        again = input("🔁 View another customer? (Y/N): ").strip().lower()
        if again != 'y':
            print("👋 Exiting RM Assist. Goodbye!")
            break

if __name__ == "__main__":
    main()
