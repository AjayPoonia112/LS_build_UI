"""Streamlit session state helpers."""
import uuid
import streamlit as st

def init_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"sess-{uuid.uuid4().hex[:12]}"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user" not in st.session_state:
        st.session_state.user = None
    if "pending_trace" not in st.session_state:
        st.session_state.pending_trace = []
