# clarifier.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clarify_query(user_query):
    prompt_path = os.path.join("prompts", "clarification_prompt.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"{prompt_path} not found")

    with open(prompt_path, "r", encoding="utf-8") as f:
        clarification_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": clarification_prompt},
            {"role": "user", "content": user_query}
        ]
    )
    clarified = response.choices[0].message.content.strip()
    print(f"\n🤖 Clarified Query:\n{clarified}")
    return clarified
