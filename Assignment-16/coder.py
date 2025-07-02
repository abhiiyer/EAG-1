from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_coder_prompt():
    with open("prompts/coder_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def run_coder_agent(insights: dict, max_calls=4):
    prompt_template = load_coder_prompt()
    history = []
    current_instruction = "Start with the Introduction"
    html_parts = []

    for i in range(max_calls):
        combined_prompt = prompt_template + "\n\n" + json.dumps(insights, indent=2) + f"\n\nInstruction: {current_instruction}"

        print(f"\n🔁 [call_self] Iteration {i+1} → {current_instruction}")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert report generator."},
                {"role": "user", "content": combined_prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        print(f"📦 Raw output {i+1}:\n", content)

        try:
            output = json.loads(content)
            html_parts.append(output["html"])
            history.append(output)

            if not output.get("call_self"):
                print("✅ No further self-calls. Report complete.")
                break

            current_instruction = output.get("next_instruction", "Continue")
        except Exception as e:
            print(f"❌ JSON parsing failed in iteration {i+1}: {e}")
            break

    final_html = "<html><body>\n" + "\n<hr>\n".join(html_parts) + "\n</body></html>"

    # Save to file
    out_path = "outputs/final_report.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\n✅ Final HTML saved to: {out_path}")
    return final_html, history
