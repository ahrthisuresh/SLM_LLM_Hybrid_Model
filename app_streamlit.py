# import streamlit as st
# from src.router import route,compare

# import time
# from src.models.slm_loader import SLM
# from src.models.llm_client import LLM   # adjust if your file name differs

# # load both models once
# slm = SLM(model_path="src/models/slm_ft")
# llm = LLM(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# def compare_models(task:str,text:str):
#     from src.router import TASKS  # import inside to avoid circular imports
#     system, build = TASKS[task]
#     prompt = build(text)
#     # SLM
#     start = time.time()
#     slm_out = slm.generate(system, user, task=task)
#     slm_time = round(time.time() - start, 3)

#     # LLM
#     start = time.time()
#     llm_out = llm.generate(system, user, task=task)
#     llm_time = round(time.time() - start, 3)

#     return {
#         "SLM": {"output": slm_out, "latency": slm_time},
#         "LLM": {"output": llm_out, "latency": llm_time}
#     }


# st.set_page_config(page_title="SLM-First Hybrid Agent", page_icon="🤖")

# st.title("SLM-First Hybrid Agent")
# task = st.selectbox("Choose task", ["extract_json", "summarize"])
# text = st.text_area("Paste text", height=220, placeholder="Paste an email, ticket, or article...")

# col1, col2 = st.columns(2)
# with col1:
#     if st.button("Compare SLM vs LLM"):
#         results = compare_models(task,text)
#         st.subheader("Comparison Results")
#         st.json(results)

#     if st.button("Run"):
#         res = route(task, text)
#         st.markdown(f"**Routed to:** `{res.route}` · **Latency:** `{res.latency_ms:.1f} ms`")
#         if task == "extract_json":
#             if res.parsed_json:
#                 st.json(res.parsed_json)
#             else:
#                 st.code(res.output)
#         else:
#             st.write(res.output)
# with col2:
#     st.markdown("### Tips")
#     st.markdown("- Short/structured → SLM\n- Long/reasoning → LLM\n- Invalid JSON → fallback to LLM")
import streamlit as st
from src.router import route, compare

st.set_page_config(page_title="SLM-First Hybrid Agent", page_icon="🤖")

st.title("SLM-First Hybrid Agent")
task = st.selectbox("Choose task", ["extract_json", "summarize"])
text = st.text_area("Paste text", height=220, placeholder="Paste an email, ticket, or article...")

col1, col2 = st.columns(2)

with col1:
    if st.button("Compare SLM vs LLM", disabled=not bool(text.strip())):
        results = compare(task, text)   # <-- uses router.compare
        st.subheader("Comparison Results")
        # pretty-print: JSON when dict, code block otherwise
        st.markdown(f"**SLM · latency:** {results['SLM']['latency_ms']} ms")
        st.json(results["SLM"]["output"])

        st.markdown(f"**LLM · latency:** {results['LLM']['latency_ms']} ms")
        if results["LLM"]["parsed_json"]:
            st.json(results["LLM"]["parsed_json"])
        else:
            st.code(results["LLM"]["output"])

    if st.button("Run (route)", disabled=not bool(text.strip())):
        res = route(task, text)
        st.markdown(f"**Routed to:** `{res.route}` · **Latency:** `{res.latency_ms:.1f} ms`")
        if task == "extract_json" and res.parsed_json:
            st.json(res.parsed_json)
        else:
            st.code(res.output if isinstance(res.output, str) else str(res.output))

with col2:
    st.markdown("### Tips")
    st.markdown("- Short/structured → SLM\n- Long/reasoning → LLM\n- Invalid JSON → fallback to LLM\n- Use **Compare** to see quality + latency side-by-side")
