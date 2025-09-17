# # import os, torch
# # from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
# # # from . import  # no-op to make relative imports explicit
# # from ..config import get_device

# # class SLM:
# #     def __init__(self, model_name=None):
# #         self.model_name = model_name or os.getenv("SLM_MODEL", "HuggingFaceTB/SmolLM2-135M")
# #         self.device = get_device()
# #         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
# #         dtype = torch.float16 if self.device in ("cuda","mps") else torch.float32
# #         self.model = AutoModelForCausalLM.from_pretrained(
# #             self.model_name, torch_dtype=dtype
# #         ).to(self.device)

# #     def generate(self, system: str, user: str, max_new_tokens=256):
# #         tok = self.tokenizer
# #         if tok.pad_token is None:
# #             tok.pad_token = tok.eos_token
# #         # simple chat-style prompt for instruction SLMs
# #         prompt = f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n[USER]\n{user}\n[/USER]\n[ASSISTANT]\n"
# #         inputs = tok(prompt, return_tensors="pt").to(self.device)
# #         out = self.model.generate(
# #             **inputs, max_new_tokens=max_new_tokens, do_sample=False
# #         )
# #         text = tok.decode(out[0], skip_special_tokens=True)
# #         return text.split("[ASSISTANT]")[-1].strip()


# # import os, torch
# # from transformers import AutoModelForCausalLM, AutoTokenizer
# # from jsonformer import Jsonformer
# # from ..config import get_device

# # # Schema for JSON extraction
# # EXTRACT_SCHEMA = {
# #     "type": "object",
# #     "properties": {
# #         "customer_name": {"type": "string"},
# #         "issue": {"type": "string"},
# #         "priority": {"type": "string", "enum": ["low", "medium", "high"]}
# #     },
# #     "required": ["customer_name", "issue", "priority"]
# # }

# # class SLM:
# #     def __init__(self, model_name=None):
# #         # self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
# #         # self.device = get_device()
# #         # self.tokenizer = AutoTokenizer.from_pretrained(self.model_name,use_fast=True)
# #         # # self.model_name = model_name or os.getenv("SLM_MODEL", "HuggingFaceTB/SmolLM2-135M")
# #         # # self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
# #         # dtype = torch.float16 if self.device in ("cuda","mps") else torch.float32
# #         # self.model = AutoModelForCausalLM.from_pretrained(
# #         #     self.model_name, torch_dtype=dtype
# #         # ).to(self.device)
# #         # pick the passed model_name or from .env
# #         self.model_name = model_name or os.getenv("SLM_MODEL", "HuggingFaceTB/SmolLM2-135M")
# #         self.device = get_device()
        
# #         # load tokenizer
# #         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
# #         if self.tokenizer.pad_token is None:
# #             self.tokenizer.pad_token = self.tokenizer.eos_token

# #         # load model
# #         dtype = torch.float16 if self.device in ("cuda", "mps") else torch.float32
# #         self.model = AutoModelForCausalLM.from_pretrained(
# #             self.model_name, torch_dtype=dtype
# #         ).to(self.device)
# #     def generate(self, system: str, user: str, task: str = "general", max_new_tokens=256):
# #         """
# #         task: 'extract_json' or 'summarize'
# #         """
# #         if task == "extract_json":
# #             # Schema-guided decoding with jsonformer
# #             prompt = f"{system}\n\n{text_clean(user)}"
# #             jsonformer = Jsonformer(self.model, self.tokenizer, EXTRACT_SCHEMA, prompt)
# #             try:
# #                 result = jsonformer()  # always valid JSON
# #                 return result
# #             except Exception as e:
# #                 return {"error": f"Schema-guided decoding failed: {str(e)}"}
# #         else:
# #             # fallback: normal text generation
# #             tok = self.tokenizer
# #             if tok.pad_token is None:
# #                 tok.pad_token = tok.eos_token
# #             prompt = f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n[USER]\n{user}\n[/USER]\n[ASSISTANT]\n"
# #             inputs = tok(prompt, return_tensors="pt").to(self.device)
# #             out = self.model.generate(
# #                 **inputs, max_new_tokens=max_new_tokens, do_sample=False
# #             )
# #             text = tok.decode(out[0], skip_special_tokens=True)
# #             return text.split("[ASSISTANT]")[-1].strip()

# # def text_clean(s: str):
# #     """Basic cleaning for input text."""
# #     return s.replace("\n", " ").strip()
# import os, torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from jsonformer import Jsonformer
# from ..config import get_device

# # Schema for JSON extraction
# EXTRACT_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "customer_name": {"type": "string"},
#         "issue": {"type": "string"},
#         "priority": {"type": "string", "enum": ["low", "medium", "high"]}
#     },
#     "required": ["customer_name", "issue", "priority"]
# }

# class SLM:
#     def __init__(self, model_name=None):
#         # ✅ ensure model_name is set (from argument OR env OR fallback)
#         path = "models/slm_ft"
#         tok = AutoTokenizer.from_pretrained(path)
#         model = AutoModelForCausalLM.from_pretrained(path)
#         print("✅ Loaded fine-tuned model from", path)
#         self.model_name = model_name or os.getenv("SLM_MODEL", "HuggingFaceTB/SmolLM2-135M")
#         self.device = get_device()

#         # load tokenizer
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
#         if self.tokenizer.pad_token is None:
#             self.tokenizer.pad_token = self.tokenizer.eos_token

#         # load model
#         dtype = torch.float16 if self.device in ("cuda", "mps") else torch.float32
#         self.model = AutoModelForCausalLM.from_pretrained(
#             self.model_name,
#             torch_dtype=dtype
#         ).to(self.device)

#     def generate(self, system: str, user: str, task: str = "general", max_new_tokens=256):
#         if task == "extract_json":
#             # schema-guided decoding
#             prompt = f"{system}\n\n{text_clean(user)}"
#             jsonformer = Jsonformer(self.model, self.tokenizer, EXTRACT_SCHEMA, prompt)
#             try:
#                 return jsonformer()
#             except Exception as e:
#                 return {"error": f"Schema-guided decoding failed: {str(e)}"}
#         else:
#             # fallback: normal text generation
#             tok = self.tokenizer
#             if tok.pad_token is None:
#                 tok.pad_token = tok.eos_token
#             prompt = f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n[USER]\n{user}\n[/USER]\n[ASSISTANT]\n"
#             inputs = tok(prompt, return_tensors="pt").to(self.device)
#             out = self.model.generate(
#                 **inputs, max_new_tokens=max_new_tokens, do_sample=False
#             )
#             text = tok.decode(out[0], skip_special_tokens=True)
#             return text.split("[ASSISTANT]")[-1].strip()

# def text_clean(s: str):
#     return s.replace("\n", " ").strip()

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from jsonformer import Jsonformer
from ..config import get_device

# Schema for JSON extraction
EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "customer_name": {"type": "string"},
        "issue": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]}
    },
    "required": ["customer_name", "issue", "priority"]
}

class SLM:
    def __init__(self, model_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # .../src/models
        default_path = os.path.join(base_dir, "slm_ft")        # .../src/models/slm_ft
        self.model_path = model_path or default_path

        self.device = get_device()

        # load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, use_fast=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # load model
        dtype = torch.float16 if self.device in ("cuda", "mps") else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=dtype
        ).to(self.device)

        print(f"✅ Loaded fine-tuned model from {self.model_path}")
    def generate(self, system: str, user: str, task: str = "general", max_new_tokens=256):
        if task == "extract_json":
            # schema-guided decoding
            prompt = f"{system}\n\n{text_clean(user)}"
            jsonformer = Jsonformer(self.model, self.tokenizer, EXTRACT_SCHEMA, prompt)
            try:
                return jsonformer()
            except Exception as e:
                return {"error": f"Schema-guided decoding failed: {str(e)}"}
        else:
            # fallback: normal text generation
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

def text_clean(s: str):
    return s.replace("\n", " ").strip()
