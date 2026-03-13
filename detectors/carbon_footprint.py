from typing import List, Dict

CARBON_INTENSITY = {
    "gpt-4o": 0.05, "gpt-4": 0.08, "claude-sonnet": 0.04,
    "gemini-pro": 0.035, "gpt-4o-mini": 0.005, "gemini-1.5-flash": 0.002
}

def detect(df, classifications) -> List[Dict]:
    findings = []
    df['co2_grams'] = df.apply(
        lambda row: (row['input_tokens'] + row['output_tokens']) / 1000 * CARBON_INTENSITY.get(row['model'], 0.02), 
        axis=1
    )
    co2_waste = df['co2_grams'].sum() * 0.4 # Simplified waste estimate
    if co2_waste > 0:
        findings.append({
            "title": "Carbon Inefficiency Tax",
            "description": "Quantifies unnecessary CO2 emissions from high-energy models. Aligning technical operations with corporate ESG goals.",
            "confidence": 0.9,
            "affected_requests": len(df),
            "evidence": f"Estimated {co2_waste:.2f}g of excess CO2.",
            "recommendation": "Transition simple workloads to 'Mini' or 'Flash' models."
        })
    return findings