from duckduckgo_search import DDGS
import json
from datetime import datetime
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "real_leads.json"

SEARCH_QUERIES = [
    "UAE startup funding 2025 site:gulfbusiness.com",
    "UAE founder raised capital site:zawya.com",
    "UAE business awards 2025 site:thenationalnews.com"
]

def extract_leads(results):
    leads = []
    for r in results:
        snippet = r.get("body", "")
        title = r.get("title", "")
        link = r.get("href", "")

        # Heuristic logic (very basic)
        name = title.split(" ")[0:2]  # assume first two words is name
        name = " ".join(name)
        company = r.get("source", "Unknown").replace("www.", "").split(".")[0].capitalize()
        city = "Dubai" if "Dubai" in snippet else "Abu Dhabi" if "Abu Dhabi" in snippet else "UAE"
        trigger = title
        source = link.split("/")[2]

        leads.append({
            "name": name,
            "company": company,
            "city": city,
            "trigger": trigger,
            "source": source
        })
    return leads

def fetch_real_leads():
    all_results = []
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            results = list(ddgs.text(query, max_results=10))
            extracted = extract_leads(results)
            all_results.extend(extracted)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"✅ Fetched {len(all_results)} real leads and saved to real_leads.json")

if __name__ == "__main__":
    fetch_real_leads()
