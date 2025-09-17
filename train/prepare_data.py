import os, json
from dotenv import load_dotenv
import openai
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are a dataset generator.
Produce synthetic customer support tickets in varied formats (emails, chat logs, casual texts).
Each entry should include:
- input: unstructured text (email/ticket)
- target: JSON with fields {customer_name, issue, priority}
Priority = high if urgent/ASAP/critical, medium if slow/degraded/intermittent, else low.
Return only JSON objects, one per line.
"""

def generate_samples(n=20, path="data/finetune/train.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        for _ in range(n):
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":SYSTEM_PROMPT},
                          {"role":"user","content":"Generate 5 examples."}],
                temperature=0.7,
                max_tokens=600
            )
            text = resp.choices[0].message.content.strip()
            # each line should be a JSON object
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        json.loads(line)  # sanity check
                        f.write(line + "\n")
                    except:
                        continue
    print(f"✅ Generated dataset at {path}")

if __name__ == "__main__":
    generate_samples(n=20)  # 20 * 5 = ~100 rows
