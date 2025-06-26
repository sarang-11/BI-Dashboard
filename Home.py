import sys
import os
import streamlit as st
import pandas as pd
from utils.data_loader import load_data

import modules.client_metrics as cm
import modules.team_performance as tp
import modules.smart_insights as si

# Ensure project root is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="BI Dashboard", layout="wide")

# Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header Text
st.markdown("""
    <div style="margin: 20px; padding: 20px; border-radius: 10px; background-color: #f5f5f5;">
        <div class="main-title">Welcome to the Business Intelligence Dashboard</div>
        <div class="subtitle">Analyze client metrics, team performance, and gain smart insights</div>
    </div>
""", unsafe_allow_html=True)

# User Data Mode Switch
data_mode = st.sidebar.radio("📁 Select Data Mode", ["Demo Data", "Upload Custom Data"])
df = None

if data_mode == "Upload Custom Data":
    uploaded_file = st.sidebar.file_uploader("📤 Upload your CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Custom data uploaded!")
    else:
        st.sidebar.warning("Waiting for file upload...")
else:
    df = load_data()
    st.sidebar.info("Using demo data.")

# Navigation
page = st.sidebar.radio("Navigate to", [
    "🏠 Home",
    "📊 Client Metrics",
    "📈 Team Performance",
    "🧠 Smart Insights"
])

if page == "🏠 Home":
    st.markdown("""
        ### How to Use This Dashboard
        - Use the sidebar to explore different analytical modules.
        - Upload your own dataset or explore the demo mode.
        - Smart insights and visualizations update automatically.
        ---
        ⚙️ Powered by Streamlit + Plotly + Pandas
    """)

elif page == "📊 Client Metrics":
    if df is not None:
        cm.app(df)
    else:
        st.warning("Please upload a valid dataset to view Client Metrics.")

elif page == "📈 Team Performance":
    if df is not None:
        tp.app(df)
    else:
        st.warning("Please upload a valid dataset to view Team Performance.")

elif page == "🧠 Smart Insights":
    if df is not None:
        si.app(df)
    else:
        st.warning("Please upload a valid dataset to view Smart Insights.")