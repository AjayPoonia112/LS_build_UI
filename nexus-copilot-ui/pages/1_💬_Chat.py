"""Compliance Manager chat with the Nexus Copilot."""
import streamlit as st
from src.auth import require_login
from src.state import init_state
from src.bedrock_client import invoke_agent

init_state()
user = require_login()

st.title("💬 Compliance Copilot")
st.caption(f"Session: `{st.session_state.session_id}`")

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🛡️" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("trace"):
            with st.expander("🔍 Agent reasoning trace"):
                for step in msg["trace"]:
                    st.json(step, expanded=False)

# Suggested prompts
if not st.session_state.messages:
    st.markdown("**Try one of these:**")
    cols = st.columns(3)
    suggestions = [
        "Reconcile Q3 EFPIA disclosures under the new €15 threshold",
        "Show all HCP identity conflicts between Veeva and Reltio",
        "What CMS rule changes were detected this week?",
    ]
    for col, prompt in zip(cols, suggestions):
        if col.button(prompt, use_container_width=True):
            st.session_state.pending_prompt = prompt
            st.rerun()

# Chat input
prompt = st.chat_input("Ask Nexus Compliance…")
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🛡️"):
        placeholder = st.empty()
        trace_events = []
        full_response = ""
        try:
            for event in invoke_agent(st.session_state.session_id, prompt):
                if event["type"] == "text":
                    full_response += event["content"]
                    placeholder.markdown(full_response + "▌")
                elif event["type"] == "trace":
                    trace_events.append(event["content"])
            placeholder.markdown(full_response)

            if trace_events:
                with st.expander("🔍 Agent reasoning trace"):
                    for step in trace_events:
                        st.json(step, expanded=False)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "trace": trace_events,
            })
        except Exception as e:
            st.error(f"Agent invocation failed: {e}")
