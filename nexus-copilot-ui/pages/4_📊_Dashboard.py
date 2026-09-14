"""Compliance operational metrics."""
import streamlit as st
from src.auth import require_login
from src.state import init_state
from src.redshift_client import query

init_state()
require_login()

st.title("📊 Compliance Dashboard")

col1, col2, col3, col4 = st.columns(4)
try:
    m = query("""
        SELECT
          COUNT(*) FILTER (WHERE status='PENDING')  AS pending,
          COUNT(*) FILTER (WHERE status='APPROVED') AS approved,
          COUNT(*) FILTER (WHERE status='REJECTED') AS rejected,
          COUNT(*)                                  AS total
        FROM ops.steward_review_queue;
    """)
    col1.metric("Pending", int(m["pending"].iloc[0]))
    col2.metric("Approved", int(m["approved"].iloc[0]))
    col3.metric("Rejected", int(m["rejected"].iloc[0]))
    col4.metric("Total", int(m["total"].iloc[0]))
except Exception as e:
    st.error(f"Dashboard load failed: {e}")

st.divider()
st.subheader("Recent Watchman alerts")
try:
    alerts = query("""
        SELECT alert_id, regulator, severity, summary, created_at
        FROM ops.watchman_alerts
        ORDER BY created_at DESC LIMIT 20;
    """)
    st.dataframe(alerts, use_container_width=True, hide_index=True)
except Exception as e:
    st.info(f"No alerts loaded: {e}")
