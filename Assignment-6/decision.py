from models import CustomerInput, RMDecision

def suggest_product_focus(rm: dict) -> str:
    gaps = {}
    for product in rm["targets"]:
        gap = rm["targets"][product] - rm["actuals"][product]
        incentive = rm["incentives"][product]
        score = (gap * incentive) / (rm["targets"][product] + 1)
        gaps[product] = score
    sorted_products = sorted(gaps.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[0][0]

def rank_customers_by_product(customers, product: str):
    filtered = [c for c in customers if product in c.products]
    ranked = sorted(filtered, key=lambda x: x.balance, reverse=True)
    return ranked

def analyze_balance_trend(history: dict) -> str:
    vals = list(history.values())
    if vals[-1] > vals[0]:
        return "growth"
    elif vals[-1] < vals[0]:
        return "drop"
    else:
        return "stable"

def generate_decision(customer: CustomerInput) -> RMDecision:
    trend = analyze_balance_trend(customer.balance_history)
    if "FX" in customer.products:
        nba = "Offer FX advisory for next AED 10K transfer"
    elif "FD" in customer.products and customer.proposed_rate > customer.int_rate:
        nba = f"Propose FD rollover at {customer.proposed_rate}%"
    elif "INV" in customer.products:
        nba = "Introduce investment webinar and advisory"
    else:
        nba = "Explore relationship deepening opportunities"

    action = nba
    msg = f"Customer {customer.name} has shown {trend} trend. Recommended: {nba}"
    return RMDecision(message=msg, suggested_action=action)