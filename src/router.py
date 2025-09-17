import time
from .models.slm_loader import SLM
from .models.llm_client import LLM
from .utils_json import try_parse_and_validate 

# Load once (uses local fine-tuned SLM at src/models/slm_ft via slm_loader)
slm = SLM() 
llm = LLM(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# ---- Tasks & prompt builders ----
def build_extract_json(text: str):
    return f"Extract customer_name, issue, and priority from this text:\n{text}"

def build_summarize(text: str):
    return f"Summarize the following text in 1–2 sentences:\n{text}"

TASKS = {
    "extract_json": ("You are an assistant that extracts structured JSON.", build_extract_json),
    "summarize": ("You are an assistant that summarizes text clearly.", build_summarize),
}

class RouteResult:
    def __init__(self, route, latency_ms, output, parsed_json=None):
        self.route = route
        self.latency_ms = latency_ms
        self.output = output
        self.parsed_json = parsed_json

# ---- SLM-first router with LLM fallback ----
def route(task: str, text: str) -> RouteResult:
    system, build = TASKS[task]
    prompt = build(text)

    t0 = time.time()
    slm_out = slm.generate(system, text, task=task)
    ms = (time.time() - t0) * 1000

    if task == "extract_json":
        parsed = None
        candidate = slm_out
        if not isinstance(candidate, dict):
            try:
                candidate = try_parse_and_validate(candidate)
            except Exception:
                candidate = None
        if candidate:
            return RouteResult("slm", ms, str(slm_out), candidate)

        # fallback to LLM
        t1 = time.time()
        llm_out = llm.generate(system, prompt, max_new_tokens=256)
        llm_ms = (time.time() - t1) * 1000
        try:
            parsed = try_parse_and_validate(llm_out)
        except Exception:
            parsed = None
        return RouteResult("llm", llm_ms, llm_out, parsed)

    # summarize path just returns SLM
    return RouteResult("slm", ms, slm_out, None)

# ---- Comparison: run BOTH models on the same input ----
def compare(task: str, text: str):
    system, build = TASKS[task]
    prompt = build(text)

    t0 = time.time()
    slm_out = slm.generate(system, text, task=task)
    slm_ms = (time.time() - t0) * 1000

    t1 = time.time()
    llm_out = llm.generate(system, prompt+ "\n\nRespond ONLY with a valid JSON object {\"customer_name\":..., \"issue\":..., \"priority\":...}. Do not add extra text.",max_new_tokens=256)
    llm_ms = (time.time() - t1) * 1000
    # Try parsing JSON for LLM
    import json
    parsed_llm = None
    try:
        parsed_llm = json.loads(llm_out)
    except Exception:
        pass

    return {
        "SLM": {"output": slm_out, "latency_ms": round(slm_ms, 1)},
        "LLM": {"output": llm_out, "latency_ms": round(llm_ms, 1), "parsed_json": parsed_llm},
    }
