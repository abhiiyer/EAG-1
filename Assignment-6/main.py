from perception import get_rm_profile
from decision import suggest_product_focus, rank_customers_by_product, generate_decision
from action import execute_action
from utils.system_prompt_builder import build_system_prompt
from utils.export_pdf import generate_pdf
from utils.email_utils import generate_email
from models import CustomerInput
import json

def load_customers():
    with open("data/rankable_customers.json", "r") as f:
        data = json.load(f)
    return [CustomerInput(**c) for c in data]

def log_interaction(rm_name, customer, decision, prompt):
    with open("rm_assist_log.txt", "a", encoding="utf-8") as log:
        log.write("\n=== Interaction Log ===\n")
        log.write(f"RM: {rm_name}\n")
        log.write(f"Customer CIF: {customer.cif}\n")
        log.write(f"Products: {', '.join(customer.products)}\n")
        log.write(f"Decision: {decision.suggested_action}\n")
        log.write(f"Message: {decision.message}\n")
        log.write(f"Prompt: {prompt.strip()}\n")

def main():
    rm = get_rm_profile()
    print(f"\nHello {rm['name']}! Here's your performance breakdown for {rm['month']}:")

    for product in ["FD", "FX", "INV"]:
        gap = rm['targets'][product] - rm['actuals'][product]
        print(f"{product}: {rm['actuals'][product]} / {rm['targets'][product]} (Gap: {gap}) - Incentive: ₹{rm['incentives'][product]}")

    while True:
        choice = input("\nWould you like me to recommend which product to focus on? (Y/N): ").strip().upper()
        if choice == "Y":
            priority_product = suggest_product_focus(rm)
            print(f"\n➡️ Based on your gaps, you should focus on **{priority_product}** customers.")
        else:
            priority_product = input("Please enter the product you want to focus on (FD/FX/INV): ").strip().upper()

        customers = load_customers()
        ranked = rank_customers_by_product(customers, priority_product)

        print("\nRecommended customers for", priority_product + ":")
        for idx, cust in enumerate(ranked):
            print(f"{idx+1}. {cust.cif} – Products: {', '.join(cust.products)} – Balance: {cust.balance}")

        selection = int(input("Choose a customer [1-N]: ")) - 1
        chosen = ranked[selection]

        prompt = build_system_prompt(rm, chosen)

        decision = generate_decision(chosen)
        execute_action(decision)
        log_interaction(rm['name'], chosen, decision, prompt)

        # Optional PDF
        if input("\nWould you like to generate a PDF for this interaction? (Y/N): ").strip().upper() == "Y":
            generate_pdf(rm['name'], chosen, decision)

        # Optional Email
        if input("Would you like to generate an email pitch for this customer? (Y/N): ").strip().upper() == "Y":
        # Dynamically compute intent_score
            score = 50
            if 'FX' in chosen.products:
                score += 10
            if chosen.balance > 100000:
                score += 10
            if 'transfer' in chosen.recent_activity.lower():
                score += 15
            if 'salary' in chosen.recent_activity.lower():
                score += 10
            intent_score = min(score, 100)
            pitch_text = f"Hi {chosen.name}, I’d like to help you get more value from your FX transfers."
            subject, body = generate_email(chosen, decision, intent_score, pitch_text)
            print("\n[EMAIL PREVIEW]")
            print("Subject:", subject)
            print("Body:", body)

        # Continue?
        again = input("\nWould you like to handle another customer? (Y/N): ").strip().upper()
        if again != "Y":
            print("Thank you. Ending session.")
            break

if __name__ == "__main__":
    main()