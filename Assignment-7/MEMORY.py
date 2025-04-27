# MEMORY.py – Manages embedding and FAISS storage

import faiss
import numpy as np
from openai import OpenAI
import os
import pickle
import tiktoken

embedding_model = "text-embedding-3-small"
index = faiss.IndexFlatL2(1536)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
url_map = []
TEXT_FOLDER = "WebText"

def get_embedding(text):
    encoding = tiktoken.encoding_for_model(embedding_model)
    tokens = encoding.encode(text)
    if len(tokens) > 8192:
        tokens = tokens[:8192]
        text = encoding.decode(tokens)
    return client.embeddings.create(input=[text], model=embedding_model).data[0].embedding

def update_index(url, text):
    print("🧠 MEMORY: Updating FAISS index")
    vector = get_embedding(text)
    index.add(np.array([vector], dtype="float32"))
    url_map.append(url)

def search_index(query):
    print("🧠 MEMORY: Querying FAISS")
    vector = get_embedding(query)
    D, I = index.search(np.array([vector], dtype="float32"), 5)
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx != -1:
            results.append((url_map[idx], dist))
    return results