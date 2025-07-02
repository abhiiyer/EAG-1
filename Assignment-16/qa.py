# qa.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question_from_html(question, html_text):
    prompt_path = os.path.join("prompts", "qaagent_prompt.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"{prompt_path} not found")

    with open(prompt_path, "r", encoding="utf-8") as f:
        qa_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": qa_prompt},
            {"role": "user", "content": f"Q: {question}\nContent:\n{html_text}"}
        ]
    )
    return response.choices[0].message.content
