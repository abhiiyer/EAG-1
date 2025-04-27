import os
import faiss
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from difflib import get_close_matches
from dotenv import load_dotenv
load_dotenv()

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
# Replace with your OpenAI key

TEXT_FOLDER = "./WebText"
os.makedirs(TEXT_FOLDER, exist_ok=True)

docs, urls = [], []
for file in os.listdir(TEXT_FOLDER):
    if file.endswith(".txt"):
        with open(os.path.join(TEXT_FOLDER, file), encoding='utf-8') as f:
            docs.append(f.read())
            urls.append(file.replace(".txt", ""))

"""
def get_openai_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding

    
def get_openai_embedding(text):
    # Limit text to ~8000 tokens = ~32000 chars
    if len(text) > 32000:
        print(f"⚠️ Text too long ({len(text)} chars). Truncating...")
        text = text[:32000]
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding
"""
import tiktoken

MAX_TOKENS = 8192
MODEL_NAME = "text-embedding-3-small"

encoding = tiktoken.encoding_for_model(MODEL_NAME)

def get_openai_embedding(text):
    tokens = encoding.encode(text)
    if len(tokens) > MAX_TOKENS:
        print(f"⚠️ Too long ({len(tokens)} tokens). Truncating to {MAX_TOKENS} tokens.")
        tokens = tokens[:MAX_TOKENS]
        text = encoding.decode(tokens)
    response = client.embeddings.create(input=[text], model=MODEL_NAME)
    return response.data[0].embedding

print(f"📄 Embedding {len(docs)} documents from WebText/")
for i, doc in enumerate(docs):
    print(f"📝 {i+1}. {urls[i]} (chars = {len(doc)})")
vectors = [get_openai_embedding(doc) for doc in docs]
dimension = len(vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors).astype("float32"))

faiss.write_index(index, "webindex.faiss")
with open("url_map.pkl", "wb") as f:
    pickle.dump(urls, f)

app = Flask(__name__)
CORS(app)

"""
def restore_url(slug):
    return slug.replace("___", "://").replace("__", "/").replace("_", ".")

def restore_url(slug):
    return slug.replace("___", "://").replace("__", "/")
"""
    
def restore_url(slug):
    return slug.replace("___", "://").replace("__", "/")



"""
@app.route("/search")
def search():
    query = request.args.get("q")
    vector = get_openai_embedding(query)
    D, I = index.search(np.array([vector]).astype("float32"), 5)

    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        url = restore_url(urls[idx])
        results.append({
            "url": url,
            "snippet": f"Score: {dist:.2f} → {url}"
        })

    return jsonify(results)
"""

"""
@app.route("/search")
def search():
    query = request.args.get("q")
    
    # Fuzzy expand using filename matches (from urls)
    all_keywords = [url.replace("___", "://").replace("__", "/").lower() for url in urls]
    expansion = get_close_matches(query, all_keywords, n=1, cutoff=0.6)
    
    if expansion:
        print(f"🔍 Expanding query '{query}' → '{expansion[0]}'")
        query = expansion[0]  # replace with better match
    else:
        print(f"🔍 No fuzzy expansion found for: {query}")


    vector = get_openai_embedding(query)
    D, I = index.search(np.array([vector]).astype("float32"), 5)

    results = []
    print("\n🔍 Search distances for query:", query)
    for dist, idx in zip(D[0], I[0]):
        print(f" → {urls[idx]} : {dist:.2f}")
        if idx == -1 or dist > 1.5:  # ✅ filter irrelevant matches
            print(f"❌ Skipping: {url} → dist = {dist:.2f}")
            continue
        url = restore_url(urls[idx])
        results.append({
            "url": url,
            "snippet": f"Score: {dist:.2f} → {url}"
        })

    return jsonify(results)
"""


"""
from difflib import get_close_matches

@app.route("/search")
def search():
    query = request.args.get("q").lower()

    # 🔍 Try to expand based on known URLs using fuzzy matching
    all_keywords = [url.replace("___", "://").replace("__", "/").lower() for url in urls]
    expansion = get_close_matches(query, all_keywords, n=1, cutoff=0.6)

    if expansion:
        print(f"🔍 Expanding query '{query}' → '{expansion[0]}'")
        query = expansion[0]
    else:
        print(f"🔍 No fuzzy expansion found for: {query}")

    # 🔗 Embed and search in FAISS
    vector = get_openai_embedding(query)
    D, I = index.search(np.array([vector]).astype("float32"), 5)

    results = []
    print("\n🔬 FAISS Results:")
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue

        url = restore_url(urls[idx])

        if dist > 1.5:
            print(f"❌ Skipping: {url} → dist = {dist:.2f}")
            continue

        print(f"✅ Showing: {url} → dist = {dist:.2f}")
        results.append({
            "url": url,
            "snippet": f"Score: {dist:.2f} → {url}"
        })

    if not results:
        print("🚫 No valid results within threshold.")

    return jsonify(results)
"""

from difflib import get_close_matches

@app.route("/search")
def search():
    query = request.args.get("q").lower()
    all_keywords = [url.replace("___", "://").replace("__", "/").lower() for url in urls]
    expansion = get_close_matches(query, all_keywords, n=1, cutoff=0.6)

    if expansion:
        print(f"🔍 Expanding query '{query}' → '{expansion[0]}'")
        query = expansion[0]
    else:
        print(f"🔍 No fuzzy expansion found for: {query}")

    vector = get_openai_embedding(query)
    D, I = index.search(np.array([vector]).astype("float32"), 5)

    results = []
    print("\n🔬 FAISS Results:")
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue

        url_key = urls[idx]
        file_path = os.path.join(TEXT_FOLDER, url_key + ".txt")

        try:
            with open(file_path, encoding="utf-8") as f:
                doc_content = f.read().lower()
            if query.lower() not in doc_content:
                print(f"❌ Skipping: {url_key} → dist = {dist:.2f} (query not in doc)")
                continue
        except Exception as e:
            print(f"⚠️ Could not open {file_path}: {e}")
            continue

        if dist > 1.5:
            print(f"❌ Skipping: {url_key} → dist = {dist:.2f} (above threshold)")
            continue

        restored_url = restore_url(url_key)
        print(f"✅ Showing: {restored_url} → dist = {dist:.2f}")

        results.append({
            "url": restored_url,  # ✅ IMPORTANT
            "snippet": f"Score: {dist:.2f} → {restored_url}"
        })

    if not results:
        print("🚫 No valid results for:", query)

    return jsonify(results)


"""
@app.route("/upload_url_text", methods=["POST"])
def upload_url_text():
    from bs4 import BeautifulSoup
    data = request.get_json()
    url = data.get("url", "")
    html = data.get("html", "")
    filename = url.replace("://", "___").replace("/", "__").replace(".", "_") + ".txt"

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    with open(os.path.join(TEXT_FOLDER, filename), "w", encoding="utf-8") as f:
        f.write(text)
    return "Saved: " + filename
"""

"""
@app.route("/upload_url_text", methods=["POST"])
def upload_url_text():
    from bs4 import BeautifulSoup
    data = request.get_json()
    
    url = data.get("url", "")
    html = data.get("html", "")
    print(f"\n📥 Received POST from Chrome extension")
    print(f"🌐 URL = {url}")
    print(f"📄 HTML Length = {len(html)}")

    filename = url.replace("://", "___").replace("/", "__").replace(".", "_") + ".txt"
    full_path = os.path.join(TEXT_FOLDER, filename)

    try:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Saved: {full_path}")
        return "Saved"
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return "Failed", 500
"""
@app.route("/upload_url_text", methods=["POST"])
def upload_url_text():
    from bs4 import BeautifulSoup
    import tiktoken
    import faiss
    import numpy as np

    data = request.get_json()
    url = data.get("url", "")
    html = data.get("html", "")
    print(f"\n📥 Received POST from Chrome extension")
    print(f"🌐 URL = {url}")
    print(f"📄 HTML Length = {len(html)}")

    filename = url.replace("://", "___").replace("/", "__") + ".txt"
    #filename = url.replace("://", "___").replace("/", "__").replace(".", "_") + ".txt"
    full_path = os.path.join(TEXT_FOLDER, filename)

    try:
        # Extract visible text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # Save file to WebText
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Saved: {full_path}")

        # 🔁 Rebuild FAISS index
        print("🔁 Rebuilding FAISS index from WebText/")
        docs, urls_local = [], []
        for file in os.listdir(TEXT_FOLDER):
            if file.endswith(".txt"):
                with open(os.path.join(TEXT_FOLDER, file), encoding="utf-8") as f:
                    content = f.read()

                    # Truncate safely using tiktoken
                    encoding = tiktoken.encoding_for_model("text-embedding-3-small")
                    tokens = encoding.encode(content)
                    if len(tokens) > 8192:
                        print(f"⚠️ File {file} too long ({len(tokens)} tokens). Truncating to 8192 tokens.")
                        tokens = tokens[:8192]
                        content = encoding.decode(tokens)
                    docs.append(content)
                    urls_local.append(file.replace(".txt", ""))

        print(f"📦 Total files embedded: {len(docs)}")

        vectors = [get_openai_embedding(doc) for doc in docs]
        dimension = len(vectors[0])
        global index, urls
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(vectors).astype("float32"))
        urls = urls_local

        print("✅ FAISS index updated.")

        return "Saved & Indexed"

    except Exception as e:
        print(f"❌ Failed: {e}")
        return "Failed", 500


if __name__ == "__main__":
    print("🔗 Running on http://localhost:5000/search?q=your_query")
    app.run(host="0.0.0.0", port=5000)
