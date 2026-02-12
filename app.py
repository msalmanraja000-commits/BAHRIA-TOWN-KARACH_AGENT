import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import plotly.graph_objects as go
import re

# 1. Page Config
st.set_page_config(page_title="Karachi Real Estate Pro", page_icon="🏛️", layout="wide")

# High-Contrast CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #111111; border: 0.5px solid #444; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Session State Initialization (Yahan 0 set kiya hai)
if "market_score" not in st.session_state:
    st.session_state.market_score = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Secure Keys
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

# 4. Sidebar with Live Gauge
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/line-chart.png")
    st.title("Elite Analytics")
    sector = st.selectbox("Market Focus:", ["DHA Karachi", "Bahria Town Karachi", "Karachi General"])
    
    st.markdown("---")
    st.subheader("Market Confidence Score")
    
    # Gauge Chart Logic
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.market_score,
        number = {'font': {'color': "white", 'size': 50}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#00ffcc" if st.session_state.market_score > 0 else "#222"},
            'bgcolor': "#111111",
            'bordercolor': "#ffffff", 'borderwidth': 1
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.market_score > 0:
        st.success(f"Live Sentiment: {st.session_state.market_score}%")
    else:
        st.info("Status: Waiting for Analysis")

# 5. Main Chat Logic
st.title("🏛️ Karachi Enterprise Advisory")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Phase 8 or Precinct 10..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Analyzing Market Intelligence...", expanded=False):
            search_res = tavily.search(query=f"latest property rates {sector} {prompt} Karachi Feb 2026", search_depth="advanced")
            intel = "\n".join([r['content'] for r in search_res['results']])
        
        system_msg = f"""
        You are a Senior Advisor. Use this data: {intel}.
        Provide professional analysis.
        MANDATORY: At the very end, add 'INTERNAL_SCORE:XX' (XX is 1-100). 
        Do not use the word SCORE alone.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        
        raw_response = completion.choices[0].message.content
        
        # --- SCORE EXTRACTION & CLEANING ---
        # 1. Pattern dhoondna
        score_match = re.search(r"INTERNAL_SCORE:(\d+)", raw_response)
        
        if score_match:
            # 2. Score update karna
            st.session_state.market_score = int(score_match.group(1))
            # 3. Response se score wala text mita dena (Ye "Safai" hai)
            final_response = re.sub(r"INTERNAL_SCORE:\d+", "", raw_response).strip()
        else:
            final_response = raw_response

        st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        st.rerun() # Refresh taake meter foran ghoome
