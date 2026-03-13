from typing import List, Dict

def detect(df, classifications) -> List[Dict]:
    findings = []
    avg_retries = df['retry_count'].mean()
    retry_rate = (df['retry_count'] > 0).mean()
    if retry_rate > 0.05 or avg_retries > 0.2:
        findings.append({
            "title": "Retry Amplification",
            "description": "This measures 'Systemic Friction'—when the AI fails and has to try again. Each retry multiplies the cost of a single transaction, essentially acting as an invisible tax on your cloud spend.",
            "confidence": 0.75,
            "affected_requests": int((df['retry_count']>0).sum()),
            "evidence": {"avg_retries": float(avg_retries), "retry_rate": float(retry_rate)},
            "recommendation": "Optimize prompts to reduce failure rates; implement smarter caching to avoid paying for the same result twice.",
        })
    return findings