"""Data Steward approvals inbox — HITL gate."""
import hashlib
from datetime import datetime
import streamlit as st
from src.auth import require_login
from src.state import init_state
from src.redshift_client import query, submit_approval
from src.config import ROLE_STEWARD

init_state()
user = require_login()

st.title("✅ Steward Approvals")

if user["role"] != ROLE_STEWARD:
    st.warning("Only Data Stewards can approve corrections. Viewing in read-only mode.")

st.caption("Corrections drafted by the Fixer agent — awaiting your review.")

# Load pending approvals
try:
    df = query("""
        SELECT approval_id, correction_set_id, reason, affected_rows,
               dq_pass_rate, pii_findings, created_at
        FROM ops.steward_review_queue
        WHERE status = 'PENDING'
        ORDER BY created_at DESC
        LIMIT 50;
    """)
except Exception as e:
    st.error(f"Failed to load approvals: {e}")
    st.stop()

if df.empty:
    st.success("🎉 No pending approvals. All clear.")
    st.stop()

for _, row in df.iterrows():
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**Correction set `{row['correction_set_id']}`**")
        c1.caption(row["reason"])
        c2.metric("Rows", int(row["affected_rows"]))
        c3.metric("DQ pass", f"{float(row['dq_pass_rate']) * 100:.1f}%")

        with st.expander("Details & audit narrative"):
            st.markdown(f"- **PII findings**: {row['pii_findings']}")
            st.markdown(f"- **Created**: {row['created_at']}")
            # Would fetch generated narrative here in full impl

        if user["role"] == ROLE_STEWARD:
            comments = st.text_input("Comments (optional)", key=f"c_{row['approval_id']}")
            b1, b2 = st.columns(2)
            if b1.button("✅ Approve", key=f"a_{row['approval_id']}", type="primary", use_container_width=True):
                sig = hashlib.sha256(
                    f"{row['approval_id']}|APPROVE|{user['email']}|{datetime.utcnow()}".encode()
                ).hexdigest()
                submit_approval(row["approval_id"], "APPROVED", user["email"], sig, comments)
                st.success(f"Approved. Signature: `sha256:{sig[:16]}…`")
                st.rerun()
            if b2.button("❌ Reject", key=f"r_{row['approval_id']}", use_container_width=True):
                sig = hashlib.sha256(
                    f"{row['approval_id']}|REJECT|{user['email']}|{datetime.utcnow()}".encode()
                ).hexdigest()
                submit_approval(row["approval_id"], "REJECTED", user["email"], sig, comments)
                st.warning("Rejected.")
                st.rerun()
