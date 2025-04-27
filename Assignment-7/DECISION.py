# DECISION.py – Filters and ranks relevant results

def select_best_results(query, results, threshold=1.5):
    print("🤖 DECISION: Selecting results")
    return [r for r in results if r[1] <= threshold]