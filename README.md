#  LLM vs SLM – Hybrid Agent

This project is a **Streamlit app** that compares a **Small Language Model (SLM)** (fine-tuned local model) against a **Large Language Model (LLM)** (TinyLlama).  
It demonstrates how requests can be **routed intelligently** between models.

---

## Getting Started

1. **Clone repo & install dependencies**
   ```
   git clone <your-repo>
   cd LLM_vs_SLM
   pip install -r requirements.txt
  

2. **Place your fine-tuned model**
   Ensure your fine-tuned model exists at:

   ```
   src/models/slm_ft/
   ├── config.json
   ├── generation_config.json
   ├── pytorch_model.bin  (or model.safetensors)
   ├── tokenizer.json
   ├── tokenizer_config.json
   ```

3. **Run the app**

   ```bash
   streamlit run app_streamlit.py
   ```

4. **Open in browser**

   ```
   http://localhost:8501
   ```

---

## 🖥️ How It Works

1. User pastes input text (e.g., support ticket, email).
2. User selects a **task**:

   * `extract_json` → extract `customer_name`, `issue`, `priority`.
   * `summarize` → generate a short summary.
3. The **router** decides:

   * Run on **SLM** first (fast + schema-guided).
   * If JSON invalid or input complex → fallback to **LLM**.
4. Optionally, run a **side-by-side comparison** of SLM vs LLM with latency metrics.

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **Streamlit** → web interface
* **Transformers (Hugging Face)** → model loading and generation
* **Jsonformer** → schema-guided JSON decoding
* **Pydantic** → structured validation
* **Fine-tuned SLM** (SmolLM2-135M)
* **TinyLlama-1.1B** as fallback LLM

---

## Why This Matters

1. Demonstrates a **hybrid agent** combining small and large models.
2. **SLM** handles structured, lightweight tasks quickly and efficiently.
3. **LLM** is used only when required → better **speed, efficiency, and cost control**.
4. Provides clear **comparison metrics** (latency + output) to evaluate trade-offs.

<img width="568" height="522" alt="image" src="https://github.com/user-attachments/assets/c8e9fc7c-e428-4dbd-8e00-69528f06b565" />
<img width="289" height="493" alt="image" src="https://github.com/user-attachments/assets/6be477f9-8e78-4eb8-9074-0b71b386ca08" />

