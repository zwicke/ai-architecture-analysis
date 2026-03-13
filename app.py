import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.data_loader import load_and_validate_csv
from classifiers.task_classifier import classify_batch

import detectors.model_overkill as model_overkill
import detectors.token_bloat as token_bloat
import detectors.carbon_footprint as carbon_footprint
import detectors.model_arbitrage as model_arbitrage
import detectors.context_overprovision as context_overprovision
import detectors.retry_amplification as retry_amplification

from cost_model.pricing import estimate_total_cost, estimate_optimized_cost

app = FastAPI(title="AI Architecture Efficiency Analyzer")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = load_and_validate_csv(io.BytesIO(contents))
        
        # 1. Enrichment
        prompts = df['prompt'].astype(str).tolist()
        classifications = classify_batch(prompts)
        
        # 2. Financials
        total_cost = estimate_total_cost(df)
        optimized = estimate_optimized_cost(df)
        
        # 3. Running Detectors with "Substance" Keys
        findings = []
        detector_modules = [
            model_overkill, token_bloat, carbon_footprint, 
            model_arbitrage, context_overprovision, retry_amplification
        ]
        
        for mod in detector_modules:
            try:
                findings += mod.detect(df, classifications)
            except Exception as e:
                print(f"Detector {mod.__name__} failed: {e}")

        # 4. Sustainability & Strategic Value
        total_co2 = float(df['co2_grams'].sum()) if 'co2_grams' in df.columns else 0.0
        # Assume $50/tonne offset price
        carbon_avoidance_value = (total_co2 * 0.45) * 0.00005 
        direct_savings = max(0.0, total_cost - optimized)

        return {
            "summary": {
                "total_requests": int(len(df)),
                "estimated_cost": round(total_cost, 4),
                "potential_savings": round(direct_savings, 4),
                "total_co2": round(total_co2, 2),
                "total_value_recovery": round(direct_savings + carbon_avoidance_value, 4)
            },
            "workload": {
                "task_distribution": pd.Series([c['task_type'] for c in classifications]).value_counts().to_dict(),
                "model_usage": df['model'].value_counts().to_dict(),
            },
            "findings": findings,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))