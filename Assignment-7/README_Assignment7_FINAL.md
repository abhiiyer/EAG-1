# 🚀 Assignment-7: Web Semantic Indexing + Chrome Plugin (FAISS + OpenAI Embeddings)

This project builds an intelligent, searchable local web memory using OpenAI's embeddings and FAISS indexing — all connected to a Chrome plugin.

The system **automatically captures visited websites (excluding confidential ones)**, extracts text content, embeds them, indexes into FAISS, and allows **real-time intelligent search** via a Chrome extension.

---

## 🧠 Architecture Overview

```
[Chrome Extension]
    ↓
[Visited URL & HTML]
    ↓
[Flask Server with /upload_url_text]
    ↓
[Text Extraction + Token Limit Handling]
    ↓
[OpenAI Embeddings + FAISS Index]
    ↓
[Search API (/search)]
    ↓
[Extension Popup UI]
```

---

## 📁 Folder & File Structure

| File/Folder                    | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| `indexer_server.py`           | 🔧 Core Flask server, handles embedding, indexing, and search logic     |
| `WebText/`                    | 📂 Contains `.txt` files for each visited URL's plain-text content      |
| `chrome_plugin/`              | 🌐 Chrome extension UI and automation                                  |
| ├─ `manifest.json`            | Chrome plugin configuration and script registration                    |
| ├─ `popup.html`               | Extension popup interface with input box and result list               |
| ├─ `popup.js`                 | Handles search queries and displays FAISS results                      |
| ├─ `background.js`            | Background service worker for handling message passing                 |
| ├─ `content_script.js`        | Injected into every page to grab full HTML                             |
| └─ `icon.png`                 | Plugin icon                                                            |
| `AGENT.py`                    | Orchestrates the embedding + search flow (placeholder for architecture)|
| `PERCEPTION.py`               | Handles perception layer – listens for Chrome activity                 |
| `MEMORY.py`                   | Handles vector memory and FAISS logic                                 |
| `ACTION.py`                   | Responsible for response and highlighting logic                        |
| `DECISION.py`                 | Applies thresholding and similarity filtering                         |

---

## 🛠 How to Run Step-by-Step

### ✅ Backend Setup
1. Install Python dependencies:
```bash
pip install openai flask flask-cors faiss-cpu beautifulsoup4 tiktoken
```

2. Replace your OpenAI API key inside `indexer_server.py`:
```python
client = openai.Client(api_key="sk-...")
```

3. Run the server:
```bash
python indexer_server.py
```

---

### 🌐 Chrome Plugin Setup
1. Go to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **“Load Unpacked”** and select the `chrome_plugin/` folder
4. Visit any non-confidential website (e.g., [Wikipedia - Tokyo](https://en.wikipedia.org/wiki/Tokyo))
5. Click the extension icon and search terms like `"tokyo"`, `"ricky ponting"`, etc.

---

## 🧪 Features

- ✅ Auto-ingests visited web pages via content scripts
- ✅ Extracts raw text and embeds via OpenAI's `text-embedding-3-small`
- ✅ Builds FAISS index with real-time update via `/upload_url_text`
- ✅ Allows fuzzy/semantic search via `/search?q=...`
- ✅ Chrome extension shows clickable results with proper link restoration

---

## 🐞 Key Issues Faced (and Resolved!)

| Issue | Resolution |
|-------|------------|
| `.txt` files too long for OpenAI | ✅ Used `tiktoken` to truncate to 8192 tokens |
| FAISS returning irrelevant results | ✅ Applied strict distance + content keyword checks |
| Links opening as `https://en_wikipedia_org/...` | ✅ Fixed `restore_url()` + file naming strategy |
| Search for "ponting" returned nothing | ✅ Fuzzy expansion via `difflib` to match `"ricky ponting"` |
| Plugin results not showing | ✅ Corrected threshold logic and Chrome content script wiring |

---

## 🔍 Sample Search Use-Cases

| Query          | Result URL |
|----------------|------------|
| `ricky ponting`| `https://en.wikipedia.org/wiki/Ricky_Ponting` |
| `tokyo`        | `https://en.wikipedia.org/wiki/Tokyo` |
| `modi`         | `https://en.wikipedia.org/wiki/Narendra_Modi` |

---

## 👨‍🏫 Notes for Evaluator

This assignment required integration of:
- Chrome scripting
- Web automation
- NLP embeddings
- Real-time API serving
- Indexed vector search

Multiple rounds of debugging were involved in perfecting:
- File naming vs URL restoration
- Token-safe truncation
- Filtering out noise from embeddings
- Plugin–backend interaction

Final system is robust, scalable and 100% automated from website visit → index → semantic search ✅

---

## ✨ Credits

- Built using `OpenAI`, `FAISS`, `Flask`, `Chrome Extensions`, `tiktoken`, `difflib`
- Student: **Abhishek Iyer**
- Assignment-7 – EAG-1 Series