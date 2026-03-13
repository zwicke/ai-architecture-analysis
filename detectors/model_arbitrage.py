from typing import List, Dict
from cost_model.benchmarks import calculate_arbitrage_opportunity

def detect(df, classifications) -> List[Dict]:
    findings = []
    savings = calculate_arbitrage_opportunity(df)
    if savings > 0:
        findings.append({
            "title": "Vendor Market Arbitrage",
            "description": "Identifies savings by switching providers for equivalent intelligence levels.",
            "confidence": 0.95,
            "affected_requests": len(df),
            "evidence": f"Potential savings: ${savings:.4f}",
            "recommendation": "Review enterprise agreements; consider multi-cloud strategy."
        })
    return findings