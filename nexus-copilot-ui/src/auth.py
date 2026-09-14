# """Cognito login — simplified for MVP."""
# import streamlit as st
# import boto3
# from botocore.exceptions import ClientError
# from src.config import AWS_REGION, COGNITO_CLIENT_ID, ROLE_MANAGER, ROLE_STEWARD, ROLE_EXECUTIVE

# def require_login():
#     """Show login form if user not authenticated. Returns user dict."""
#     if st.session_state.get("user"):
#         _sidebar_user_info()
#         return st.session_state.user

#     st.title("🔐 Sign in to Nexus Compliance")
#     with st.form("login"):
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         submit = st.form_submit_button("Sign in", type="primary")

#     if submit:
#         try:
#             # For MVP demo — swap to real Cognito USER_SRP_AUTH in prod
#             client = boto3.client("cognito-idp", region_name=AWS_REGION)
#             resp = client.initiate_auth(
#                 ClientId=COGNITO_CLIENT_ID,
#                 AuthFlow="USER_PASSWORD_AUTH",
#                 AuthParameters={"USERNAME": email, "PASSWORD": password},
#             )
#             token = resp["AuthenticationResult"]["IdToken"]
#             # Decode ID token claims (skipped here — use python-jose in prod)
#             st.session_state.user = {
#                 "email": email,
#                 "name": email.split("@")[0].title(),
#                 "role": _resolve_role(email),
#                 "token": token,
#             }
#             st.rerun()
#         except ClientError as e:
#             st.error(f"Login failed: {e.response['Error']['Message']}")
#     st.stop()

# def _resolve_role(email: str) -> str:
#     # Demo shortcut — in prod, read from Cognito group claim
#     if "steward" in email:
#         return ROLE_STEWARD
#     if "exec" in email:
#         return ROLE_EXECUTIVE
#     return ROLE_MANAGER

# def _sidebar_user_info():
#     u = st.session_state.user
#     with st.sidebar:
#         st.markdown(f"**👤 {u['name']}**")
#         st.caption(u["role"].replace("_", " ").title())
#         if st.button("Sign out", use_container_width=True):
#             st.session_state.clear()
#             st.rerun()

"""Demo auth for MVP — replace with real Cognito for production."""
import streamlit as st

# Hardcoded demo users for build-a-thon
DEMO_USERS = {
    "manager@nexus.demo": {
        "password": "Demo123!",
        "name": "Alex Manager",
        "role": "compliance_manager",
    },
    "steward@nexus.demo": {
        "password": "Demo123!",
        "name": "Jamie Steward",
        "role": "data_steward",
    },
    "exec@nexus.demo": {
        "password": "Demo123!",
        "name": "Chris Executive",
        "role": "compliance_executive",
    },
}

def require_login():
    """Show login form; returns user dict when authenticated."""
    if st.session_state.get("user"):
        _sidebar_user_info()
        return st.session_state.user

    st.title("🔐 Sign in to Nexus Compliance")
    st.caption("Demo credentials below — for build-a-thon MVP only")

    with st.expander("ℹ️ Demo credentials"):
        st.code("""
manager@nexus.demo   / Demo123!   (Compliance Manager)
steward@nexus.demo   / Demo123!   (Data Steward - can approve)
exec@nexus.demo      / Demo123!   (Compliance Executive)
        """)

    with st.form("login"):
        email = st.text_input("Email", placeholder="manager@nexus.demo")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)

    if submit:
        user_record = DEMO_USERS.get(email.lower().strip())
        if user_record and user_record["password"] == password:
            st.session_state.user = {
                "email": email.lower().strip(),
                "name": user_record["name"],
                "role": user_record["role"],
                "token": "demo-token",
            }
            st.success(f"Welcome, {user_record['name']}!")
            st.rerun()
        else:
            st.error("Invalid credentials. See demo credentials above.")
    st.stop()

def _sidebar_user_info():
    u = st.session_state.user
    with st.sidebar:
        st.markdown(f"**👤 {u['name']}**")
        st.caption(u["role"].replace("_", " ").title())
        if st.button("Sign out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
