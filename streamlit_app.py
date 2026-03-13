import streamlit as st
import pandas as pd
import plotly.express as px
import io
from collections import Counter

# --- Internal Module Imports ---
# Ensure these folders and __init__.py files are in your GitHub repo
from utils.data_loader import load_and_validate_csv
from classifiers.task_classifier import classify_batch
import detectors.model_overkill as model_overkill
import detectors.token_bloat as token_bloat
import detectors.carbon_footprint as carbon_footprint
import detectors.model_arbitrage as model_arbitrage
from cost_model.pricing import estimate_total_cost, estimate_optimized_cost

# --- Page Config ---
st.set_page_config(
    page_title="AI Architecture Efficiency Analyzer",
    page_icon="🏗️",
    layout="wide"
)

# --- Navigation Tabs ---
tab_overview, tab_audit = st.tabs(["📄 Strategic Overview", "📊 Live Audit Dashboard"])

# --- TAB 1: STRATEGIC OVERVIEW ---
with tab_overview:
    st.title("🏗️ AI Architecture Efficiency Analyzer")
    st.markdown("---")
    
    st.header("What This Tool Does")
    st.write("""
    The **AI Architecture Efficiency Analyzer** is a diagnostic platform for understanding the economic performance of your AI architecture.
    
    As AI adoption accelerates, organizations are rapidly accumulating an invisible cost center: the **Inflexibility Tax**. This is the margin erosion that occurs when a 'Ferrari-class' model is used for a 'bicycle-class' problem. The Analyzer audits production AI logs to expose these inefficiencies and provide a clear diagnostic of how efficiently your organization is deploying intelligence.
    """)

    st.header("From Cost Monitoring to AI Architecture Governance")
    st.write("""
    Traditional FinOps tools focus on tracking spend. **This Analyzer focuses on *why* the spend exists in the first place.** By analyzing task routing, the platform surfaces structural inefficiencies and provides a roadmap for right-sizing the AI stack.
    """)

    st.header("Sustainability-Adjusted ROI")
    st.write("""
    Beyond direct cost savings, the platform introduces a **Sustainability-Adjusted ROI** metric. Architectural efficiency reduces the energy intensity of AI workloads, quantifying both **Financial savings** and **Carbon avoidance**.
    """)

    st.markdown("---")
    col_use, col_val = st.columns(2)
    with col_use:
        st.subheader("How to Use")
        st.markdown("1. **Upload Logs** | 2. **Automated Analysis** | 3. **Strategic Audit**")
    with col_val:
        st.subheader("Why It Delivers Value")
        st.success("**Margin Recovery** | **ESG Transparency** | **Procurement Leverage**")

# --- TAB 2: AUDIT DASHBOARD (Merged Logic) ---
with tab_audit:
    st.header("Strategic Audit Dashboard")
    
    with st.sidebar:
        st.header("Data Ingestion")
        uploaded = st.file_uploader("Upload Production Logs", type=["csv"])

    if uploaded:
        with st.spinner("Processing Analytics Engine Locally..."):
            try:
                # 1. Load Data
                df = load_and_validate_csv(io.BytesIO(uploaded.getvalue()))
                
                # 2. Enrichment & Task Classification
                prompts = df['prompt'].astype(str).tolist()
                classifications = classify_batch(prompts)
                
                # 3. Financials
                total_cost = estimate_total_cost(df)
                optimized = estimate_optimized_cost(df)
                
                # 4. Diagnostic Detectors
                findings = []
                detector_modules = [model_overkill, token_bloat, carbon_footprint, model_arbitrage]
                for mod in detector_modules:
                    try:
                        findings += mod.detect(df, classifications)
                    except Exception as e:
                        st.warning(f"Detector {mod.__name__} encountered a non-critical error.")

                # 5. Summary Stats
                total_co2 = float(df['co2_grams'].sum()) if 'co2_grams' in df.columns else 0.0
                carbon_avoidance_val = (total_co2 * 0.45) * 0.00005 
                direct_savings = max(0.0, total_cost - optimized)
                total_recovery = direct_savings + carbon_avoidance_val

                # --- RENDER METRICS ---
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Requests", f"{len(df):,}")
                m2.metric("Current Spend", f"${total_cost:,.4f}")
                roi_pct = (total_recovery / total_cost * 100) if total_cost > 0 else 0
                m3.metric("Strategic Value Recovery", f"${total_recovery:,.2f}", delta=f"{roi_pct:.1f}% Adj. ROI")
                m4.metric("Carbon Footprint", f"{total_co2:.1f}g CO2e", delta="ESG Impact")

                st.divider()

                # --- VISUALIZATIONS ---
                c_left, c_right = st.columns(2)
                with c_left:
                    task_counts = Counter([c['task_type'] for c in classifications])
                    task_df = pd.DataFrame.from_dict(task_counts, orient='index', columns=['count']).reset_index()
                    st.plotly_chart(px.pie(task_df, values='count', names='index', title='Workload Distribution', hole=0.4), use_container_width=True)
                with c_right:
                    model_counts = df['model'].value_counts().to_dict()
                    model_df = pd.DataFrame.from_dict(model_counts, orient='index', columns=['count']).reset_index()
                    st.plotly_chart(px.bar(model_df, x='index', y='count', title='Model Utilization', color='index'), use_container_width=True)

                # --- FINDINGS ---
                st.subheader("Diagnostic Audit Findings")
                for f in findings:
                    with st.expander(f"⚠️ {f.get('title')} (Impact: {f.get('affected_requests')} Requests)"):
                        c_tech, c_strat = st.columns(2)
                        with c_tech:
                            st.markdown("**🛠️ Technical Root Cause**")
                            st.write(f.get('technical_analysis', "Detailed technical logs processed."))
                        with c_strat:
                            st.markdown("**📈 Strategic Impact**")
                            st.write(f.get('description', "Assessing organizational impact."))
                        st.info(f"**Executive Recommendation:** {f.get('recommendation')}")

            except Exception as e:
                st.error(f"Critical Engine Error: {e}")
    else:
        st.info("👈 Please upload your production logs in the sidebar to begin.")