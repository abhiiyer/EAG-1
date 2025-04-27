# ACTION.py – Finalizes and formats result presentation

def present_results(results):
    print("🎯 ACTION: Formatting output")
    return [{
        "url": url,
        "snippet": f"Score: {dist:.2f} → {url}"
    } for url, dist in results]