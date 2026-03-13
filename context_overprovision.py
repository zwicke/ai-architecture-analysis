from typing import List, Dict

CONTEXT_LIMITS = {
    "gpt-4o": 128000,
    "gpt-4": 8192,
    "gemini-pro": 1000000,
    "claude-sonnet": 200000,
}

def detect(df, classifications) -> List[Dict]:
    findings = []
    rows = []
    for i, row in df.iterrows():
        model = row['model']
        limit = CONTEXT_LIMITS.get(model, 8192)
        utilization = (row['input_tokens'] or 0) / float(limit)
        if utilization < 0.10:
            rows.append({"index": i, "model": model, "utilization": utilization})
    if rows:
        findings.append({
            "title": "Context Overprovisioning",
            "description": "This flags requests where we are paying for massive data processing capacity but only utilizing a small fraction of it. It represents 'Reserved Capacity Waste' where the architecture is not right-sized for the data being processed.",
            "confidence": 0.8,
            "affected_requests": len(rows),
            "evidence": rows[:10],
            "recommendation": "Switch to models with smaller default windows for these tasks or batch smaller requests together.",
        })
    return findings