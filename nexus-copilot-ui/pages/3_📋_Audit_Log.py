"""Immutable audit log viewer."""
import streamlit as st
from src.auth import require_login
from src.state import init_state
from src.redshift_client import query

init_state()
user = require_login()

st.title("📋 Audit Log")
st.caption("Immutable record of every regulated change — regulator-defensible.")

col1, col2 = st.columns(2)
regulator = col1.selectbox("Regulator", ["All", "CMS", "EFPIA", "JPMA"])
limit = col2.slider("Rows", 10, 500, 100)

where = "" if regulator == "All" else f"WHERE regulator = '{regulator}'"
df = query(f"""
    SELECT audit_id, event_type, regulator, approver, signature_hash, created_at
    FROM ops.audit_log
    {where}
    ORDER BY created_at DESC
    LIMIT {limit};
""")

st.dataframe(df, use_container_width=True, hide_index=True)
st.download_button("⬇️ Export CSV", df.to_csv(index=False), "audit_log.csv")
