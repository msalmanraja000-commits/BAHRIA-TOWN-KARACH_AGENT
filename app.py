import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import plotly.graph_objects as go

# 1. Page Config with Ultra-Black Corporate Theme
st.set_page_config(page_title="Karachi Real Estate Intelligence", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-weight: 300; }
    .stChatMessage { background-color: #111111; border: 0.5px solid #333; border-radius: 4px; padding: 20px; }
    .stMetric { border-left: 3px solid #00ffcc; padding-left: 10px; }
    /* Corporate Table Style */
    .styled-table { margin: 25px 0; font-size: 0.9em; min-width: 400px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Secure Initialization
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

# 3. Sidebar: Market Selection & Analytics
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/city-buildings.png")
    st.title("Elite Analytics")
    sector = st.selectbox("Select Strategy Area:", ["DHA Karachi", "Bahria Town Karachi", "Karachi General"])
    
    st.markdown("---")
    st.subheader("Investor Sentiment")
    # Gauge Chart for Maxout Feel
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 78,
        title = {'text': "Buying Confidence", 'font': {'color': "white"}},
        gauge = {'axis': {'range': [None, 100], 'tickcolor': "white"},
                 'bar': {'color': "#00ffcc"},
                 'bgcolor': "#111111",
                 'steps': [{'range': [0, 50], 'color': "#333"}]}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"})
    st.plotly_chart(fig, use_container_width=True)

# 4. Intelligence Engine
def fetch_corporate_intel(query, area):
    search_q = f"Latest investment analysis {area} {query} prices tax Feb 2026"
    return tavily.search(query=search_q, search_depth="advanced")

# 5. Main Interface
st.title("🏛️ Karachi Enterprise Advisory")
st.caption(f"Logged in: Senior Investment Consultant | Focus: {sector}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Analyze Phase 8 vs Precinct 10..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Accessing Private Market Data...", expanded=False):
            intel = fetch_corporate_intel(prompt, sector)
        
        system_msg = f"""
        Identity: Senior Real Estate Strategist for High-Net-Worth Individuals.
        Focus: {sector}. 
        Context: {intel}
        Rule: If comparing DHA and Bahria, provide a Table. 
        Formatting: Use bold headers and clean bullet points.
        Ending: Always offer a 'Strategic Site Visit'.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        
        response = completion.choices[0].message.content
        st.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
