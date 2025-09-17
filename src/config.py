import os, torch

def get_device():
    pref = os.getenv("DEVICE", "auto").lower()
    if pref == "mps" and torch.backends.mps.is_available(): return "mps"
    if pref == "cuda" and torch.cuda.is_available(): return "cuda"
    if pref == "auto":
        if torch.cuda.is_available(): return "cuda"
        if torch.backends.mps.is_available(): return "mps"
    return "cpu"
