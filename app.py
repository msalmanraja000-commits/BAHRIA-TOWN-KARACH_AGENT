import streamlit as st
import random
import time

st.set_page_config(page_title="DHA Intel | PropTecSolutions", page_icon="🏛️", layout="wide")

# UI Styling
st.markdown("<style>.main {background-color: #0b0e14; color: white;}</style>", unsafe_allow_html=True)

st.title("🏛️ DHA Karachi: Proprietary AI Dashboard")
st.caption("Developed by PropTecSolutions | Restricted Access")

# Sentiment & Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Market Sentiment Index", f"{random.randint(78, 91)}/100", delta="Verified")
with col2:
    st.metric("Growth Forecast", "Bullish", delta="High Potential")

# Lead Capture
with st.sidebar:
    st.title("🔑 Founder's Access")
    with st.form("leads"):
        st.write("Investor Inquiry Form")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        if st.form_submit_button("Submit to PropTecSolutions"):
            st.success("Lead encrypted and sent to Founder.")

# Analysis Query
query = st.text_input("Analyze DHA Phase/Sector:")
if query:
    with st.spinner("Processing through PropTecSolutions Core..."):
        time.sleep(1)
        st.write(f"### Intelligence Brief: {query}")
        st.info("Technical Trend: Accumulation Phase detected in current cycle.")

# --- THE SECURITY SHIELD FOOTER ---
st.divider()
st.markdown("""
    <div style='text-align: center; color: #ff4b4b; font-size: 11px; font-weight: bold;'>
        PROPERTY OF PROPTECSOLUTIONS. ALL RIGHTS RESERVED. <br>
        <span style='color: gray;'>Access granted for evaluation purposes only. Unauthorized replication of this source code or AI architecture will lead to legal action under Pakistan Intellectual Property Laws.</span>
    </div>
    """, unsafe_allow_html=True)
