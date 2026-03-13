from typing import List, Dict


def detect(df, classifications) -> List[Dict]:
    findings = []
    repeated = df['request_id'].duplicated().sum()
    if repeated > 0 or df['retry_count'].mean() > 0.5:
        findings.append({
            "title": "Agent Overuse",
            "confidence": 0.7,
            "affected_requests": int(repeated),
            "evidence": {"repeated_request_ids": int(repeated)},
            "recommendation": "Reduce chained agent calls; consolidate logic server-side",
        })
    return findings
