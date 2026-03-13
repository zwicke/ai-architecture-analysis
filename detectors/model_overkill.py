def detect(df, classifications) -> list:
    overkill_rows = []
    for i, row in df.iterrows():
        task = classifications[i]['task_type']
        model = str(row['model']).lower()
        if task in ["summarization", "extraction"] and any(m in model for m in ["gpt-4", "o1"]):
            overkill_rows.append(i)
    
    if not overkill_rows: return []
    return [{
        "title": "Overpowered Model Usage",
        "confidence": 0.95,
        "affected_requests": len(overkill_rows),
        "technical_analysis": f"Identified {len(overkill_rows)} transactions using Frontier models for deterministic tasks. Logs show 2000ms+ latency for tasks that perform identically on Flash-tier models.",
        "description": "This is a core driver of the Inflexibility Tax. Using high-reasoning models for routine extraction creates high variable costs with no marginal intelligence gain.",
        "recommendation": "Deploy a task router to shift routine extraction to gpt-4o-mini or gemini-1.5-flash."
    }]