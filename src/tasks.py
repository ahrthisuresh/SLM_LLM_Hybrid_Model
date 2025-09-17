from .prompts import EXTRACT_JSON_SYSTEM, SUMMARIZE_SYSTEM

def build_extract_prompt(text: str):
    return f"Extract JSON from the following text:\n---\n{text}\n---"

def build_summarize_prompt(text: str):
    return f"Summarize the following text:\n---\n{text}\n---"

TASKS = {
  "extract_json": (EXTRACT_JSON_SYSTEM, build_extract_prompt),
  "summarize":    (SUMMARIZE_SYSTEM,    build_summarize_prompt),
}
