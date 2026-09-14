"""Cognito login — simplified for MVP."""
import streamlit as st
import boto3
from botocore.exceptions import ClientError
from src.config import AWS_REGION, COGNITO_CLIENT_ID, ROLE_MANAGER, ROLE_STEWARD, ROLE_EXECUTIVE

def require_login():
    """Show login form if user not authenticated. Returns user dict."""
    if st.session_state.get("user"):
        _sidebar_user_info()
        return st.session_state.user

    st.title("🔐 Sign in to Nexus Compliance")
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign in", type="primary")

    if submit:
        try:
            # For MVP demo — swap to real Cognito USER_SRP_AUTH in prod
            client = boto3.client("cognito-idp", region_name=AWS_REGION)
            resp = client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": email, "PASSWORD": password},
            )
            token = resp["AuthenticationResult"]["IdToken"]
            # Decode ID token claims (skipped here — use python-jose in prod)
            st.session_state.user = {
                "email": email,
                "name": email.split("@")[0].title(),
                "role": _resolve_role(email),
                "token": token,
            }
            st.rerun()
        except ClientError as e:
            st.error(f"Login failed: {e.response['Error']['Message']}")
    st.stop()

def _resolve_role(email: str) -> str:
    # Demo shortcut — in prod, read from Cognito group claim
    if "steward" in email:
        return ROLE_STEWARD
    if "exec" in email:
        return ROLE_EXECUTIVE
    return ROLE_MANAGER

def _sidebar_user_info():
    u = st.session_state.user
    with st.sidebar:
        st.markdown(f"**👤 {u['name']}**")
        st.caption(u["role"].replace("_", " ").title())
        if st.button("Sign out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
