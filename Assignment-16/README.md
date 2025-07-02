# 💡 Mashreq Strategy Copilot (Assignment 16 + Real-World Banking Use-Case)

This project is a **multi-agent system** that:
- ✅ Fulfills **Assignment-16** requirements (call_self, multi-agent pipeline, HTML output)
- ✅ Solves a real Mashreq business problem: **"Understand Competitor Strategy for Liabilities, FX, Investment, and Insurance"**

---

## 🔧 How It Works (Architecture)

```
PlannerAgent → RetrieverAgent → ThinkerAgent → CoderAgent (call_self loop) → FormatterAgent
```

| Agent         | Description |
|---------------|-------------|
| **PlannerAgent**   | Converts query into actionable steps |
| **RetrieverAgent** | Uses Google Programmable Search to fetch relevant articles |
| **ThinkerAgent**   | Extracts FX, Investment, Insurance, and Liability strategy themes |
| **CoderAgent**     | Builds the HTML report in 4 sections using `call_self` logic (up to 4 calls) |
| **FormatterAgent** | Final polish and consistent styling |

---


## 🗂️ File-wise Purpose and Example Usage

| File Name     | Purpose                                                      | Example                                                              |
|:--------------|:-------------------------------------------------------------|:---------------------------------------------------------------------|
| main.py       | Entry point. Takes a query, runs full pipeline.              | Query = 'Mashreq FX vs FAB 2025'                                     |
| clarifier.py  | Clarifies the original query using GPT.                      | 'Mashreq FX' → 'Compare Mashreq's FX pricing vs FAB for 2025 in UAE' |
| retriever.py  | Searches web via Google Search API and extracts raw text.    | Search: 'Mashreq FX strategy 2025 site:thenationalnews.com'          |
| distiller.py  | Summarizes retrieved articles into clean chunks.             | Input: raw HTML → Output: bullet summary per article                 |
| planner.py    | Extracts business insights or themes from the summaries.     | Themes: FX innovation, digital onboarding, pricing transparency      |
| coder.py      | Uses call_self to build sections of HTML report per insight. | Insight → 'Mashreq's FX fees are above market' → 1 section in HTML   |
| formatter.py  | Applies styling to the final HTML report.                    | Adds color, spacing, fonts to the report                             |
| qa.py         | Lets user ask follow-up questions about the report.          | Q: 'Which bank had better FX growth?' → Answer from HTML             |
| summarizer.py | Creates 5-line executive summary for leadership.             | FX fees are high, digital channel lagging, ENBD gaining share...     |
| /prompts/     | Folder with prompt templates for each agent.                 | `clarification_prompt.txt`, `summarizer_prompt.txt`, etc.            |
| /outputs/     | Final HTML and TXT files are saved here.                     | `formatted_report.html`, `summary.txt`                               |

---

### ✨ Key Enhancements in This Version

- ✅ `call_self` logic in `coder.py` upgraded to allow up to **4 recursive calls**
- ✅ Custom logging added to show recursive self-calls in console output
- ✅ **Q&A capability** added post-report generation (via `qa.py`)
- ✅ **Executive summary** saved to `outputs/summary.txt`
- ✅ Clean folder structure: `/prompts`, `/outputs`, all agents modularized

---

## 🧪 Sample Query Used

```txt
Mashreq Bank competitors strategy on Liabilities and revenue (FX/Investment/Insurance) and what should Mashreq do
```

---

## 📁 Folder Structure

```
mashreq_agent/
├── main.py                   # Main entry point
├── clarifier.py              # Clarifies vague queries using GPT
├── retriever.py              # Article retriever using Google API + Trafilatura
├── distiller.py              # Summarizes retrieved articles into key points
├── planner.py                # PlannerAgent - breaks query into strategic plan
├── coder.py                  # HTML builder agent using call_self (recursive)
├── formatter.py              # Beautifies HTML report with clean formatting
├── qa.py                     # Question Answering agent (post-report Q&A)
├── summarizer.py             # Executive 5-line summary for leadership
├── utils.py                  # Common utilities and helper functions
├── executor.py               # Executes plans and logs output (optional)
├── prompts/                  # Prompt files used by each agent
│   ├── clarification_prompt.txt
│   ├── distiller_prompt.txt
│   ├── qaagent_prompt.txt
│   ├── summarizer_prompt.txt
│   ├── retriever_prompt.txt
│   ├── executor_prompt.txt
├── outputs/                  # Final HTML reports and summary saved here
│   ├── formatted_report.html
│   ├── summary.txt
├── .env                      # Your OpenAI + Google API keys (excluded from repo)
```

---

## 🚀 How to Run

### 1. 🧱 Install Dependencies

```bash
pip install openai google-api-python-client python-dotenv beautifulsoup4
```

### 2. 🔑 Add `.env` File

Create a `.env` in root folder:

```env
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-search-api-key
GOOGLE_CX=your-cx-id
```

### 3. ▶️ Run Main File

```bash
python main.py
```

---

## 📄 Assignment Checklist ✅

| Requirement                                  | Status |
|----------------------------------------------|--------|
| `call_self` logic (with max 4 calls)         | ✅ Yes |
| JSON-based agent planning/execution          | ✅ Yes |
| Multi-agent architecture                     | ✅ Yes |
| Article retrieval and summarization          | ✅ Yes |
| Final HTML report saved                      | ✅ Yes |
| Prompt files organized                       | ✅ Yes |
| GitHub-ready code with modular files         | ✅ Yes |

---

## 💼 Business Use-Case for Mashreq

This tool helps **Mashreq’s analytics or strategy team**:
- Monitor competitor actions in FX, Insurance, and Liabilities
- Get monthly HTML summaries from public sources
- Empower RMs or strategy leads to react fast to FAB, ENBD, ADCB tactics

---


## ✅ Final Output

After running, check:
```
outputs/final_report.html          ← Basic version
outputs/formatted_report.html      ← Polished HTML (title + sections)
```

Open either file in browser 🎉

---

### 🧠 Optional Future Enhancements

1. Add voice input for question entry
2. Turn the final HTML into a Streamlit dashboard
3. Automate browser search using Browser Agent
4. Push summaries monthly to GitHub or email
5. Highlight bank-level trends using color-coding inside HTML

---

## 📞 Questions?

Drop a mail to abhishekr.iyer88@gmail.com or contact your LLM/Assignment mentor.

## 🎓 Assignment-16: Explicit Breakdown of Requirements Met

Your professor specified the following:

> 1. **"CoderAgent is still using old structure. Move to call_self with changes."**

✅ **Done** — `coder.py` now uses `call_self` recursion to build the final HTML.  
Each call processes a section like: `Liabilities`, `FX`, `Investments`, `Insurance`.

---

> 2. **"call_self is limited to 2 calls... change that to 4."**

✅ **Done** — We implemented support for **up to 4 `call_self` invocations**, controlled via a `MAX_CALL_SELF = 4` variable.  
The loop terminates automatically after 4 logical sections.

---

> 3. **"Show a use-case where CoderAgent is called more than 2 times (log not present, add that)."**

✅ **Done** — Logs clearly show each `call_self` iteration like:

```txt
[CoderAgent] Generating section: Liabilities
[CoderAgent] Generating section: FX
[CoderAgent] Generating section: Investments
[CoderAgent] Generating section: Insurance
```

You can visually validate this in the HTML report or console output.

---

> 4. **"Submit any detailed report generated by the code (HTML)."**

✅ **Done** — The final output `formatted_report.html` is a clean, full report on:
**"Mashreq Bank vs Competitor Strategy in Liabilities, FX, Investment, Insurance"**

---

> 5. **"GitHub should show original commit + your updated one."**

✅ **Ready** — Your GitHub upload should show:
- Initial commit with base code
- Final commit with planner/thinker/coder/formatter logic + prompt files

---


---

Made with 💼 by [Abhishek Iyer] for both learning and real-world banking strategy.
