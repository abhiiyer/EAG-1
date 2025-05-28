import json
import time
from pathlib import Path

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))   # Path(__file__).resolve().parent.parent takes you up to your root folder hni_lead_generator/


from utils import config

from playwright.sync_api import sync_playwright

#DATA_PATH = Path(__file__).parent.parent / "data" / "fake_leads.json"

if config.USE_REAL_LEADS:
    DATA_PATH = Path(__file__).parent.parent / "data" / "real_leads.json"
else:
    DATA_PATH = Path(__file__).parent.parent / "data" / "fake_leads.json"


FORM_URL = "http://localhost:5000/form"

def submit_lead(lead, page):
    page.goto(FORM_URL)
    page.fill('input[name="name"]', lead["name"])
    page.fill('input[name="company"]', lead["company"])
    page.fill('input[name="city"]', lead["city"])
    page.fill('input[name="trigger"]', lead["trigger"])
    page.fill('input[name="source"]', lead["source"])
    
    '''
    # Enrichment fields (optional)
    page.evaluate("document.querySelector('input[name=linkedin_url]').value = '" + lead.get("linkedin_url", "") + "'")
    page.evaluate("document.querySelector('input[name=contact_email]').value = '" + lead.get("contact_email", "") + "'")
    page.evaluate("document.querySelector('input[name=company_website]').value = '" + lead.get("company_website", "") + "'")
    page.evaluate("document.querySelector('input[name=has_contact]').value = '" + str(lead.get("has_contact", False)) + "'")
    '''
    
    
    page.evaluate("document.querySelector('input[name=data_source]').value = '" + lead["data_source"] + "'")
    page.click('input[type="submit"]')
    page.wait_for_timeout(1000)  # wait for a second before next

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        leads = json.load(f)
        # Add source tag to each lead
    for lead in leads:
        lead["data_source"] = "REAL" if config.USE_REAL_LEADS else "FAKE"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for lead in leads:
            print(f"Submitting lead: {lead['name']} - {lead['company']}")
            submit_lead(lead, page)
        browser.close()

if __name__ == "__main__":
    main()
