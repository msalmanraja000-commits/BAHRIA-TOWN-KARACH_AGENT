import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import plotly.graph_objects as go
import re

# 1. Page Config & Professional Dark Theme
st.set_page_config(page_title="Karachi Real Estate Intelligence", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stChatMessage { background-color: #111111; border: 0.5px solid #444; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Secure Initialization
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error("API Keys Missing! Check Streamlit Secrets.")
    st.stop()

# 3. Session State for Score (Start at 0)
if "market_score" not in st.session_state:
    st.session_state.market_score = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar: Elite Analytics
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/line-chart.png")
    st.title("Elite Analytics")
    sector = st.selectbox("Market Focus:", ["DHA Karachi", "Bahria Town Karachi", "Karachi General"])
    
    st.markdown("---")
    st.subheader("Market Confidence Score")
    
    # Dynamic Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.market_score,
        number = {'font': {'color': "white", 'size': 50}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#00ffcc" if st.session_state.market_score > 0 else "#444"},
            'bgcolor': "#111111",
            'bordercolor': "#ffffff",
            'borderwidth': 1,
            'steps': [{'range': [0, 100], 'color': "#000000"}]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.market_score == 0:
        st.caption("Waiting for analysis... (Ask about a Phase or Precinct)")
    else:
        st.success(f"Live Sentiment: {st.session_state.market_score}%")

# 5. Main Advisor Interface
st.title("🏛️ Karachi Enterprise Advisory")
st.caption(f"Strategy Module Active | Area: {sector}")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Logic
if prompt := st.chat_input("Ask about Phase 8 rates, Precinct 10 analysis, etc..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Live Search
        with st.status(f"Scanning {sector} Market Data...", expanded=False):
            search_query = f"Latest property rates and investment news {sector} {prompt} Karachi Feb 2026"
            search_results = tavily.search(query=search_query, search_depth="advanced")
            intel = "\n".join([r['content'] for r in search_results['results']])
        
        # System Prompt to Extract Score
        system_msg = f"""
        You are a Senior Strategic Advisor for Karachi Real Estate. 
        Sector: {sector}
        Live Data: {intel}
        
        Instructions:
        1. Provide a professional, corporate analysis.
        2. Use tables if comparing prices.
        3. At the VERY END of your response, you MUST write 'SCORE:XX' where XX is a number between 1-100 
           representing the investment confidence for the area mentioned.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        
        full_response = completion.choices[0].message.content
        
        # Extract Score and Update Gauge
        score_match = re.search(r"SCORE:(\d+)", full_response)
        if score_match:
            st.session_state.market_score = int(score_match.group(1))
            # Clean the response so 'SCORE:XX' doesn't look ugly to the user
            clean_response = full_response.replace(score_match.group(0), "").strip()
        else:
            clean_response = full_response

        st.markdown(clean_response)
        st.session_state.messages.append({"role": "assistant", "content": clean_response})
        
        # Trigger UI Rerun to update Gauge in sidebar
        st.rerun()
