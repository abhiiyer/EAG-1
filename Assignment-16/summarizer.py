# summarizer.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_html_report(html_content):
    prompt_path = os.path.join("prompts", "summarizer_prompt.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"{prompt_path} not found")

    with open(prompt_path, "r", encoding="utf-8") as f:
        summarizer_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": summarizer_prompt},
            {"role": "user", "content": html_content}
        ]
    )

    summary = response.choices[0].message.content.strip()
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n🧾 Executive Summary saved as outputs/summary.txt")
    return summary
