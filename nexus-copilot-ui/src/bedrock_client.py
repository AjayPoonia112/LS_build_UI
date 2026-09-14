"""Bedrock Agent InvokeAgent wrapper with streaming."""
import json
import boto3
from src.config import AWS_REGION, BEDROCK_AGENT_ID, BEDROCK_AGENT_ALIAS_ID

_client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

def invoke_agent(session_id: str, prompt: str, enable_trace: bool = True):
    """
    Streams response chunks from a Bedrock Agent.
    Yields dicts: {"type": "text"|"trace", "content": ...}
    """
    resp = _client.invoke_agent(
        agentId=BEDROCK_AGENT_ID,
        agentAliasId=BEDROCK_AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt,
        enableTrace=enable_trace,
    )

    for event in resp.get("completion", []):
        if "chunk" in event:
            data = event["chunk"]["bytes"].decode("utf-8")
            yield {"type": "text", "content": data}
        elif "trace" in event and enable_trace:
            yield {"type": "trace", "content": event["trace"]}
