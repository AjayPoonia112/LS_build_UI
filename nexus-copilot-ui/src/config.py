"""Environment configuration."""
import os

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
BEDROCK_AGENT_ID = os.getenv("BEDROCK_AGENT_ID", "AGENTXXXX")
BEDROCK_AGENT_ALIAS_ID = os.getenv("BEDROCK_AGENT_ALIAS_ID", "TSTALIASID")
REDSHIFT_WORKGROUP = os.getenv("REDSHIFT_WORKGROUP", "nexus-wg")
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE", "compliance")
REDSHIFT_SECRET_ARN = os.getenv("REDSHIFT_SECRET_ARN", "")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "")

# Roles
ROLE_MANAGER = "compliance_manager"
ROLE_STEWARD = "data_steward"
ROLE_EXECUTIVE = "compliance_executive"
