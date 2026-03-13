import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Configuration ---
API_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="AI Architecture Efficiency Analyzer",
    page_icon="🏗️",
    layout="wide"
)

# --- Main Navigation Tabs ---
tab_overview, tab_audit = st.tabs(["📄 Strategic Overview", "📊 Live Audit Dashboard"])

with tab_overview:
    st.title("🏗️ AI Architecture Efficiency Analyzer")
    st.markdown("---")
    
    # Section 1: What This Tool Does
    st.header("What This Tool Does")
    st.write("""
    The **AI Architecture Efficiency Analyzer** is a diagnostic platform for understanding the economic performance of your AI architecture.
    
    As AI adoption accelerates across the enterprise, organizations are rapidly accumulating an invisible new cost center: the architecture layer that determines how intelligence is allocated across tasks. In most systems, high-frontier models are routinely deployed for workloads that require only basic reasoning—creating hidden structural inefficiencies.
    
    The result is what we call the **Inflexibility Tax**: the margin erosion that occurs when AI systems lack the routing, sizing, and orchestration needed to match the right level of intelligence to each task. 
    
    **In simple terms, it’s the cost of using a Ferrari-class model for a bicycle-class problem.**
    
    The Analyzer audits production AI usage logs to expose these inefficiencies. It identifies where architectural choices—such as model selection, context allocation, retry patterns, and agent design—are inflating costs without improving outcomes. The result is a clear diagnostic of how efficiently your organization is deploying intelligence.
    """)

    # Section 2: Strategy Shift
    st.header("From Cost Monitoring to AI Architecture Governance")
    st.write("""
    Traditional FinOps tools focus on tracking spend. **The AI Architecture Efficiency Analyzer instead focuses on *why* the spend exists in the first place.**
    
    By analyzing how tasks are routed across models and workloads, the platform surfaces structural inefficiencies and provides a roadmap for right-sizing the AI stack—using smaller models, dynamic routing, and leaner context strategies where appropriate. This transforms AI infrastructure from a reactive cost center into a governable strategic system.
    """)

    # Section 3: Sustainability
    st.header("Sustainability-Adjusted ROI")
    st.write("""
    Beyond direct cost savings, the platform introduces a **Sustainability-Adjusted ROI** metric. Architectural efficiency does not only reduce API costs—it also reduces the energy intensity of AI workloads. 
    
    By estimating the carbon footprint of model usage and highlighting opportunities to shift to lighter-weight models, the Analyzer quantifies both:
    * **Financial savings**
    * **Carbon avoidance**
    
    For leadership teams, this enables a **Total Value narrative** that aligns AI operations with both profitability and ESG commitments.
    """)

    st.markdown("---")

    # Section 4: Use & Value (Three-Column Layout)
    col_use, col_val = st.columns(2)
    
    with col_use:
        st.subheader("How to Use the Analyzer")
        st.markdown("""
        1.  **Upload Production Logs**: Upload a CSV export containing model names, prompt/response tokens, and retry counts.
        2.  **Automated Task Analysis**: The system evaluates if the selected model was appropriately sized for the task profile.
        3.  **Strategic Audit Generation**: The dashboard calculates your Inflexibility Tax and generates a roadmap for margin recovery.
        """)
        
    with col_val:
        st.subheader("Why It Delivers Value")
        st.success("**Margin Recovery**: Identify immediate opportunities to route routine workloads to efficient models.")
        st.success("**ESG Transparency**: Quantify carbon footprint and provide empirical data for sustainability reporting.")
        st.success("**Procurement Leverage**: Reveal vendor pricing gaps to negotiate contracts or diversify providers.")

# --- TAB 2: AUDIT DASHBOARD ---
with tab_audit:
    st.header("Strategic Audit Dashboard")
    
    with st.sidebar:
        st.header("Data Ingestion")
        uploaded = st.file_uploader("Upload Production Logs", type=["csv"])

    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue())}
        with st.spinner("Analyzing Architecture & Calculating Sustainability ROI..."):
            try:
                resp = requests.post(API_URL, files=files, timeout=45)
                resp.raise_for_status()
                report = resp.json()
                s = report['summary']
                
                # --- Metrics ---
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Requests", f"{s['total_requests']:,}")
                m2.metric("Current Spend", f"${s['estimated_cost']:,.4f}")
                val = s.get('total_value_recovery', 0)
                roi_pct = (val / s['estimated_cost'] * 100) if s['estimated_cost'] > 0 else 0
                m3.metric("Strategic Value Recovery", f"${val:,.2f}", delta=f"{roi_pct:.1f}% Adj. ROI")
                m4.metric("Carbon Footprint", f"{s.get('total_co2', 0):.1f}g CO2e", delta="ESG Impact")

                st.divider()

                # --- High Substance Findings ---
                st.subheader("Diagnostic Audit Findings")
                for f in report['findings']:
                    with st.expander(f"⚠️ {f.get('title')} (Impact: {f.get('affected_requests')} Requests)"):
                        # Substance split: Technical vs Strategic
                        c_tech, c_strat = st.columns(2)
                        with c_tech:
                            st.markdown("**🛠️ Technical Root Cause**")
                            st.write(f.get('technical_analysis', "Detailed technical logs being processed..."))
                        with c_strat:
                            st.markdown("**📈 Strategic Impact**")
                            st.write(f.get('description', "Assessing organizational impact..."))
                        
                        st.info(f"**Executive Recommendation:** {f.get('recommendation')}")

            except Exception as e:
                st.error(f"Analysis Failed: {e}")
    else:
        st.info("👈 Please upload your production logs in the sidebar to begin.")