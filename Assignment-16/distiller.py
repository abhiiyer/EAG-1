# distiller.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def distill_article(article_text):
    prompt_path = os.path.join("prompts", "distiller_prompt.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"{prompt_path} not found")

    with open(prompt_path, "r", encoding="utf-8") as f:
        distiller_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": distiller_prompt},
            {"role": "user", "content": article_text}
        ]
    )
    return response.choices[0].message.content.strip()
