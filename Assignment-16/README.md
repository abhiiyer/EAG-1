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

## 🧪 Sample Query Used

```txt
Mashreq Bank competitors strategy on Liabilities and revenue (FX/Investment/Insurance) and what should Mashreq do
```

---

## 📁 Folder Structure

```
mashreq_agent/
├── main.py                   # Main entry point
├── planner.py                # PlannerAgent logic
├── retriever.py              # Article retriever using Google API
├── thinker.py                # Insight extraction agent
├── coder.py                  # HTML builder agent with call_self logic
├── formatter.py              # HTML beautifier
├── prompts/                  # Prompt files used by each agent
│   ├── planner_prompt.txt
│   ├── thinker_prompt.txt
│   ├── coder_prompt.txt
│   └── formatter_prompt.txt
├── outputs/                  # Final HTML reports saved here
├── .env                      # Your OpenAI + Google API keys (not included in repo)
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

## 🛠️ Optional Files for Future

These files are present but unused in this pipeline. They can be activated for bonus features:

| File         | Purpose                      |
|--------------|------------------------------|
| `qa.py`      | Run validation checks on output |
| `executor.py`| Execute custom code generation |
| `distiller.py`| Extract tables or summaries from PDFs |
| `clarification_prompt.txt` | Add user follow-up flow |
| `summarizer_prompt.txt` | Dedicated summarizer agent prompt |

---

## ✅ Final Output

After running, check:
```
outputs/final_report.html          ← Basic version
outputs/formatted_report.html      ← Polished HTML (title + sections)
```

Open either file in browser 🎉

---

## 📦 GitHub Submission Tip

Ensure the repo shows:
1. ✅ Original commit from prof's base
2. ✅ Your latest commit with all logic and prompt enhancements

---

## 📞 Questions?

Drop a mail to abhishekr.iyer88@gmail.com or contact your LLM/Assignment mentor.

---

Made with 💼 by [Abhishek Iyer] for both learning and real-world banking strategy.
