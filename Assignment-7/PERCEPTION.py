# PERCEPTION.py – Captures browser signals or incoming data

from bs4 import BeautifulSoup

def capture_url_and_html(url, html):
    print(f"👁️ PERCEPTION: Capturing from {url}")
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text