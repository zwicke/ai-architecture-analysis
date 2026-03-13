import streamlit as st
import pandas as pd
import plotly.express as px
import io
from collections import Counter

# --- Internal Module Imports ---
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
tab_about, tab_use = st.tabs(["📄 Learn about the Tool", "📊 Use the Tool"])

# --- TAB 1: LEARN ABOUT THE TOOL ---
with tab_about:
    st.title("🏗️ AI Architecture Efficiency Analyzer")
    st.markdown("---")
    
    # Section 1
    st.subheader("What This Tool Does")
    st.write("""
    The AI Architecture Efficiency Analyzer is a diagnostic platform for understanding the economic performance of your AI architecture.
    
    As AI adoption accelerates across the enterprise, organizations are rapidly accumulating an invisible new cost center: the architecture layer that determines how intelligence is allocated across tasks. In most systems, high-frontier models are routinely deployed for workloads that require only basic reasoning—creating hidden structural inefficiencies.
    
    The result is what we call the **Inflexibility Tax**: the margin erosion that occurs when AI systems lack the routing, sizing, and orchestration needed to match the right level of intelligence to each task.
    
    **In simple terms, it’s the cost of using a Ferrari-class model for a bicycle-class problem.**
    
    The Analyzer audits production AI usage logs to expose these inefficiencies. It identifies where architectural choices—such as model selection, context allocation, retry patterns, and agent design—are inflating costs without improving outcomes.
    
    The result is a clear diagnostic of how efficiently your organization is deploying intelligence.
    """)

    # Section 2
    st.subheader("From Cost Monitoring to AI Architecture Governance")
    st.write("""
    Traditional FinOps tools focus on tracking spend. The AI Architecture Efficiency Analyzer instead focuses on **why the spend exists in the first place.**
    
    By analyzing how tasks are routed across models and workloads, the platform surfaces structural inefficiencies and provides a roadmap for right-sizing the AI stack—using smaller models, dynamic routing, and leaner context strategies where appropriate.
    
    This transforms AI infrastructure from a reactive cost center into a governable strategic system.
    """)

    # Section 3
    st.subheader("Sustainability-Adjusted ROI")
    st.write("""
    Beyond direct cost savings, the platform introduces a **Sustainability-Adjusted ROI metric.**
    
    Architectural efficiency does not only reduce API costs—it also reduces the energy intensity of AI workloads. By estimating the carbon footprint of model usage and highlighting opportunities to shift to lighter-weight models, the Analyzer quantifies both:
    """)
    st.markdown("""
    * **Financial savings**
    * **Carbon avoidance**
    """)
    st.write("""
    For leadership teams, this enables a **Total Value narrative** that aligns AI operations with both profitability and ESG commitments.
    """)

    st.markdown("---")

    # Section 4
    col_how, col_why = st.columns(2)
    
    with col_how:
        st.subheader("How to Use the Analyzer")
        st.markdown("""
        The platform is designed for a zero-configuration audit, moving from raw data to executive insights in three steps.

        **1. Upload Production Logs**
        Upload a CSV export of AI usage containing model names, prompt/response tokens, and retry counts.

        **2. Automated Task Analysis**
        The system analyzes each request to determine its task profile (e.g., summarization, extraction, reasoning) and evaluates whether the selected model was appropriately sized.

        **3. Strategic Audit Generation**
        The dashboard calculates your Inflexibility Tax, highlights architectural inefficiencies, and generates a roadmap for margin recovery through improved model routing and stack optimization.
        """)

    with col_why:
        st.subheader("Why It Delivers Value")
        
        st.markdown("#### 💰 Margin Recovery")
        st.write("Identify immediate opportunities to route routine workloads to efficient models (Mini / Flash) without sacrificing quality.")
        
        st.markdown("#### 🌱 ESG Transparency")
        st.write("Quantify the carbon footprint of inefficient AI architecture and provide empirical data for sustainability reporting.")
        
        st.markdown("#### ⚖️ Procurement Leverage")
        st.write("Reveal vendor pricing gaps and dependency risks, giving leadership data to negotiate contracts or diversify model providers.")

# --- TAB 2: USE THE TOOL ---
with tab_use:
    st.header("Strategic Audit Dashboard")
    
    with st.sidebar:
        st.header("Data Ingestion")
        uploaded = st.file_uploader("Upload Production Logs", type=["csv"])

    if uploaded:
        with st.spinner("Processing AI Governance Audit..."):
            try:
                # Engine Execution
                df = load_and_validate_csv(io.BytesIO(uploaded.getvalue()))
                prompts = df['prompt'].astype(str).tolist()
                classifications = classify_batch(prompts)
                
                total_cost = estimate_total_cost(df)
                optimized = estimate_optimized_cost(df)
                
                findings = []
                detector_modules = [model_overkill, token_bloat, carbon_footprint, model_arbitrage]
                for mod in detector_modules:
                    try: findings += mod.detect(df, classifications)
                    except: continue

                # Summary Logic
                total_co2 = float(df['co2_grams'].sum()) if 'co2_grams' in df.columns else 0.0
                carbon_val = (total_co2 * 0.45) * 0.00005 
                direct_savings = max(0.0, total_cost - optimized)
                total_recovery = direct_savings + carbon_val

                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Requests", f"{len(df):,}")
                m2.metric("Current Spend", f"${total_cost:,.4f}")
                m3.metric("Total Strategic Value", f"${total_recovery:,.2f}", delta="Sustainability Adjusted")
                m4.metric("Carbon Footprint", f"{total_co2:.1f}g CO2e", delta="ESG Impact")

                st.divider()

                # Findings Render
                st.subheader("Diagnostic Findings")
                for f in findings:
                    with st.expander(f"⚠️ {f.get('title')} (Impact: {f.get('affected_requests')} Requests)"):
                        c_t, c_s = st.columns(2)
                        with c_t:
                            st.markdown("**🛠️ Technical Root Cause**")
                            st.write(f.get('technical_analysis'))
                        with c_s:
                            st.markdown("**📈 Strategic Impact**")
                            st.write(f.get('description'))
                        st.info(f"**Executive Recommendation:** {f.get('recommendation')}")

            except Exception as e:
                st.error(f"Engine Error: {e}")
    else:
        st.info("👈 Please upload your logs in the sidebar to begin the live audit.")