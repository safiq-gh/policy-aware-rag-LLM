import streamlit as st
import json
from rag_guard.runtime.secure_chat import secure_chat


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Prompt Injection Guard",
    layout="wide"
)

st.title("🛡️ Prompt Injection Guard Dashboard")


# -------------------------------------------------
# PROMPT INPUT
# -------------------------------------------------
prompt = st.text_area(
    "User Prompt",
    height=120,
    placeholder="Enter prompt to evaluate..."
)


# -------------------------------------------------
# EXECUTE
# -------------------------------------------------
if st.button("Run Guard") and prompt:

    with st.spinner("Running guard pipeline..."):
        result = secure_chat(prompt)

    guard = result["guard"]
    decision = guard["decision"]["action"]

    # -------------------------------------------------
    # DECISION BADGE
    # -------------------------------------------------
    color_map = {
        "allow": "🟢",
        "warn": "🟡",
        "restrict": "🟠",
        "block": "🔴"
    }

    st.subheader(f"{color_map.get(decision, '')} Decision: {decision.upper()}")

    # -------------------------------------------------
    # FINAL RESPONSE
    # -------------------------------------------------
    st.markdown("### Final Response")
    if result["mode"] == "block":
        st.write(result["reply"])
    else:
        st.write_stream(result["stream"])


    # -------------------------------------------------
    # RETRIEVED POLICIES
    # -------------------------------------------------
    with st.expander("Retrieved Policies"):
        for p in guard["policies_retrieved"]:
            st.write(p)

    # -------------------------------------------------
    # EVALUATOR OUTPUT
    # -------------------------------------------------
    with st.expander("Evaluator Output"):
        try:
            st.json(json.loads(guard["evaluator_output"]))
        except:
            st.write(guard["evaluator_output"])
