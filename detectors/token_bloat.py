def detect(df, classifications) -> list:
    bloated = df[df['input_tokens'] > df['output_tokens'] * 20]
    if bloated.empty: return []
    return [{
        "title": "Instructional Token Bloat",
        "confidence": 0.88,
        "affected_requests": len(bloated),
        "technical_analysis": "Requests show an input-to-output ratio exceeding 20:1. This indicates 'Prompt Pollution' where static system instructions are being passed repeatedly.",
        "description": "This increases operational friction and compute waste. You are paying to send the model information it has already processed in previous turns.",
        "recommendation": "Implement RAG or Prompt Caching to reduce the instructional overhead per request."
    }]