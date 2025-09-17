import os, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from ..config import get_device

class LLM:
    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("LLM_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.device = get_device()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
        dtype = torch.float16 if self.device in ("cuda","mps") else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, torch_dtype=dtype
        ).to(self.device)

    def generate(self, system: str, user: str, max_new_tokens=512):
        tok = self.tokenizer
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        prompt = f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n[USER]\n{user}\n[/USER]\n[ASSISTANT]\n"
        inputs = tok(prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False
        )
        text = tok.decode(out[0], skip_special_tokens=True)
        return text.split("[ASSISTANT]")[-1].strip()
