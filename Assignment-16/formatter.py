from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_formatter_prompt():
    with open("prompts/formatter_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def run_formatter_agent(raw_html: str) -> str:
    prompt = load_formatter_prompt() + "\n\nRaw HTML:\n" + raw_html

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional HTML formatter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    final_html = response.choices[0].message.content.strip()
    out_path = "outputs/formatted_report.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"🎨 FormatterAgent saved: {out_path}")
    return final_html
