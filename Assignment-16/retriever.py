import os
import requests
from dotenv import load_dotenv
import trafilatura

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

def google_search(query: str, num_results: int = 5):
    print(f"🔍 Searching Google for: {query}")
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": num_results
    }

    response = requests.get(search_url, params=params)
    results = response.json().get("items", [])
    
    
    print("📦 Raw Search Result Count:", len(results))
    for item in results:
        print("🔗", item.get("link"))
        
    return [item["link"] for item in results if "link" in item]

def extract_article_text(url: str):
    try:
        downloaded = trafilatura.fetch_url(url)
        return trafilatura.extract(downloaded) if downloaded else None
    except Exception:
        return None

def run_retriever_agent(query: str, top_n: int = 3):
    urls = google_search(query, num_results=top_n)
    clean_articles = []
    
    print("🔗 Raw URLs from Google API:")
    for url in urls:
        print("-", url)


    for url in urls:
        content = extract_article_text(url)
        if content:
            clean_articles.append({
                "url": url,
                "content": content.strip()[:3000]
            })

    print(f"✅ Retrieved {len(clean_articles)} articles.")
    return clean_articles
