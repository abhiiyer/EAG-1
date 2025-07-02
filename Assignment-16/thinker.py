from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_thinker_prompt():
    with open("prompts/thinker_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def run_thinker_agent(article_chunks: list) -> dict:
    combined_text = "\n\n".join([a['content'] for a in article_chunks])[:6000]  # Limit token size
    prompt = load_thinker_prompt().replace("<article_texts_here>", combined_text)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a strategic banking analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    try:
        content = response.choices[0].message.content.strip()
        print("🧠 ThinkerAgent Output:\n", content)
        return eval(content)  # or use json.loads if needed
    except Exception as e:
        print(f"❌ ThinkerAgent parsing failed: {e}")
        return {}
