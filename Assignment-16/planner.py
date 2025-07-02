from openai import OpenAI
import os
import json

from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt():
    with open("prompts/planner_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def run_planner_agent(user_query: str) -> dict:
    prompt = load_prompt().replace("<user_query>", user_query)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI agent planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    try:
        output = response.choices[0].message.content.strip()
        print("🔧 Raw LLM Output:\n", output)

        # Try to parse JSON safely
        plan_graph = json.loads(output)
        return plan_graph

    except Exception as e:
        print(f"❌ Failed to parse output: {e}")
        return {}
