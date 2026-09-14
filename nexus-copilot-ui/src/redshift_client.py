"""Redshift Data API wrapper for approvals + audit reads."""
import time
import boto3
import pandas as pd
from src.config import AWS_REGION, REDSHIFT_WORKGROUP, REDSHIFT_DATABASE, REDSHIFT_SECRET_ARN

_rs = boto3.client("redshift-data", region_name=AWS_REGION)

def query(sql: str, params: list | None = None) -> pd.DataFrame:
    kwargs = dict(
        WorkgroupName=REDSHIFT_WORKGROUP,
        Database=REDSHIFT_DATABASE,
        Sql=sql,
    )
    if REDSHIFT_SECRET_ARN:
        kwargs["SecretArn"] = REDSHIFT_SECRET_ARN
    if params:
        kwargs["Parameters"] = [{"name": f"p{i}", "value": str(v)} for i, v in enumerate(params)]

    r = _rs.execute_statement(**kwargs)
    sid = r["Id"]

    while True:
        d = _rs.describe_statement(Id=sid)
        if d["Status"] in ("FINISHED", "FAILED", "ABORTED"):
            break
        time.sleep(0.5)

    if d["Status"] != "FINISHED":
        raise RuntimeError(d.get("Error", "Redshift query failed"))

    if not d.get("HasResultSet"):
        return pd.DataFrame()

    result = _rs.get_statement_result(Id=sid)
    cols = [c["name"] for c in result["ColumnMetadata"]]
    rows = [[list(v.values())[0] if v else None for v in row] for row in result["Records"]]
    return pd.DataFrame(rows, columns=cols)

def submit_approval(approval_id: str, decision: str, approver: str, signature: str, comments: str = ""):
    sql = """
    UPDATE ops.steward_review_queue
       SET status = :p0, approver = :p1, signature_hash = :p2,
           comments = :p3, decided_at = CURRENT_TIMESTAMP
     WHERE approval_id = :p4;
    """
    query(sql, params=[decision, approver, signature, comments, approval_id])
