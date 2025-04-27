# AGENT.py – Coordinates Perception, Memory, Decision, and Action

from PERCEPTION import capture_url_and_html
from MEMORY import update_index, search_index
from DECISION import select_best_results
from ACTION import present_results

def process_new_page(url, html):
    print("🧠 AGENT: Processing new page")
    doc_text = capture_url_and_html(url, html)
    update_index(url, doc_text)

def handle_search(query):
    print("🧠 AGENT: Handling search")
    raw_results = search_index(query)
    filtered = select_best_results(query, raw_results)
    return present_results(filtered)