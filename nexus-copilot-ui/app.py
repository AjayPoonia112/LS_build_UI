"""Nexus Compliance Copilot — Home page."""
import streamlit as st
from src.auth import require_login
from src.state import init_state

st.set_page_config(
    page_title="Nexus Compliance Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_state()
user = require_login()

st.title("🛡️ Nexus Compliance Copilot")
st.caption("Sense • Validate • Fix — governed compliance for CMS, EFPIA, JPMA")

col1, col2, col3 = st.columns(3)
col1.metric("Active Pipelines", 12, "+2")
col2.metric("Pending Approvals", 4, "-1")
col3.metric("Audit Coverage", "99.8%", "+0.3%")

st.divider()

st.markdown(f"""
### Welcome, {user['name']}
Role: **{user['role']}**

Use the sidebar to navigate:
- **💬 Chat** — Ask the Copilot to reconcile, analyze, or fix
- **✅ Approvals** — Review and sign off pending corrections (Steward)
- **📋 Audit Log** — Immutable compliance history
- **📊 Dashboard** — Operational metrics
""")

st.info("💡 Try asking: *'Reconcile Q3 EFPIA disclosures under the new €15 threshold.'*")
