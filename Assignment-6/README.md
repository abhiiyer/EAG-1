# 🧠 RM Assist Plugin – Final Enhanced Version

> A complete cognitive assistant for Relationship Managers (RMs) to intelligently engage with customers using banking data, LLMs, and logic-based reasoning.

---

## 📌 Features Overview

| Layer | Description |
|-------|-------------|
| 🧠 Perception | Uses LLM (e.g., ChatGPT) to reason step-by-step and generate structured output |
| 🗂️ Memory | Pulls from customer profiles, balance trends, transaction history |
| 🤖 Decision-Making | Prioritizes product (FD/FX/INV) based on RM targets and customer signals |
| 🏃 Action | Suggests pitch, generates email & PDF, triggers call-to-action |

---

## 🚀 Flow Summary

1. RM enters name (e.g., "Sana")
2. System shows RM’s monthly performance and gaps
3. Auto-suggests which product (FD/FX/INV) to focus on
4. Shows best-matched customers for that product
5. RM selects a customer → Assistant generates:
    - Suggested Action
    - Message to RM
    - Intent score
    - Pitch script
    - PDF + email

---

## 🧪 Cognitive Prompt Structure

```text
You are an RM Assist agent.
User is Abhishek from Dubai.
They care about: savings, FDs, investments.
Goal for today: grow balances, retain FD customers.

Please reason step-by-step.
Provide output as structured JSON.
Self-check your logic before responding.
```

---

## ✨ Key Enhancements (Beyond Basics)

| Capability | Details |
|------------|---------|
| ✅ Customer Filtering | By RM target gaps and customer product match |
| ✅ Name + CIF Shown | In CMD recommendation |
| ✅ System Prompt | Shown in CMD for assignment clarity |
| ✅ Reasoning Block | Visible in output |
| ✅ Engagement Score | Auto-calculated based on balance/activity |
| ✅ PDF Export | Named as `rm_customer_date.pdf`, stored in `pdf_exports/` |
| ✅ Email Generation | To RM and customer (`.eml` files for demo) |
| ✅ Risk Alerts | Balance drop, competitor transfers, FD maturity |
| ✅ Competitor Benchmark | Simulated FX/FD rate comparison with Wio/Liv |
| ✅ Personalized Offer | FD offers based on employer (e.g., Etisalat → 4.5%) |

---

## 📁 Folder Structure

```
├── main.py
├── models.py
├── utils/
│   ├── export_pdf.py
│   ├── email_utils.py
├── data/
│   ├── rm_performance.json
│   ├── rankable_customers.json
├── pdf_exports/
│   └── <rm_customer_date>.pdf
├── email_to_rm_preview.eml
├── email_to_customer_preview.eml
```

---

## 📸 Sample CMD Output

```
Recommended customers for FX:
1. CIF0001 – Zainab – Balance: 98000.0
2. CIF0002 – Ali – Balance: 58000.0

[SYSTEM PROMPT]
...

[AGENT ACTION]
Suggested Action: Offer FX advisory for next AED 10K transfer
Message to RM: Customer Ali has shown drop trend...
```

---

## 📤 Sample Email Outputs

✔ Included in the ZIP:
- `email_to_rm_preview.eml`
- `email_to_customer_preview.eml`

Can be opened in:
- Outlook
- Thunderbird
- Notepad

---

## 🧾 Sample PDF Export

Includes:
- Customer Summary
- Risk Alerts
- Transaction Table
- Recommended Pitch
- Engagement Score
- Employer & Campaign History

Saved as:
```
pdf_exports/Abhishek_Zainab_20240708.pdf
```

---

## ✅ How to Run

1. Install dependencies:
```bash
pip install fpdf
```

2. Run the assistant:
```bash
python main.py
```

3. Answer prompts for:
   - PDF generation
   - Email preview generation

---

## 📬 Note on Gmail Sending (Optional)

To send real emails from Gmail:
- Enable 2FA
- Generate an App Password
- Update `email_utils.py` with your app password

---

## 🧑‍🏫 Ideal for Presentation / Assignments

This project demonstrates:
- Cognitive architecture
- Structured prompts
- Pydantic usage
- Multi-layer reasoning
- Banking application logic

---

> Built as part of cognitive agent assignment for RM Assist Banking Agent.