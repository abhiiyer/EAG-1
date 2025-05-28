
import re
import json
from pathlib import Path
from duckduckgo_search import DDGS

# Load scraped real leads
input_path = Path(__file__).parent.parent / "data" / "real_leads.json"
output_path = Path(__file__).parent.parent / "data" / "enriched_real_leads_generated.json"

if not input_path.exists():
    raise FileNotFoundError("Missing real_leads.json")

with open(input_path, "r", encoding="utf-8") as f:
    leads = json.load(f)
leads = leads[:1]  # ✅ Limit to first 3 leads for now to avoid hitting rate limit

enriched_leads = []

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

def search_top_result(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    time.sleep(3)  # ← Add a 2-second delay to avoid rate-limiting    
    return results

def extract_email_from_text(text):
    matches = re.findall(EMAIL_REGEX, text)
    return matches[0] if matches else ""

for lead in leads:
    name = lead.get("name", "")
    company = lead.get("company", "")
    query_base = f"{name} {company}"

    linkedin_url = ""
    results = search_top_result(f"{query_base} site:linkedin.com/in")
    for r in results:
        if "linkedin.com/in" in r.get("href", ""):
            linkedin_url = r["href"]
            break

    contact_email = ""
    company_website = ""
    results = search_top_result(f"{company} contact")
    for r in results:
        snippet = r.get("body", "") + " " + r.get("href", "")
        if not contact_email:
            contact_email = extract_email_from_text(snippet)
        if not company_website and "http" in r.get("href", ""):
            company_website = r["href"]

    lead["linkedin_url"] = linkedin_url
    lead["contact_email"] = contact_email
    lead["company_website"] = company_website
    lead["has_contact"] = bool(linkedin_url or contact_email)
    enriched_leads.append(lead)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(enriched_leads, f, indent=2)

print(f"✅ Enriched {len(enriched_leads)} leads → {output_path.name}")
