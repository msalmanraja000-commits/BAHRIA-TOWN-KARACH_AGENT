import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import plotly.graph_objects as go

st.markdown("""
    <style>
    /* Global Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    
    /* Global White Text for Sidebar */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Ensuring the Chat Input is also visible */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
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
# Sidebar Gauge: Black Background with White Text Contrast
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 78,
        number = {'font': {'color': "white", 'size': 60}}, # Score ab White aur Bara hoga
        title = {'text': "Buying Confidence", 'font': {'color': "white", 'size': 20}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': "#00ffcc"}, # Teal bar for professional look
            'bgcolor': "#111111", # Dark background inside gauge
            'bordercolor': "#333333",
            'steps': [
                {'range': [0, 100], 'color': "#000000"}] # Pure Black steps for contrast
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#161b22', # Sidebar ka dark color
        plot_bgcolor='#161b22',
        margin=dict(l=20, r=20, t=50, b=20),
        font={'color': "white", 'family': "Arial"}
    )
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

# --- Chat Logic mein ye tabdeeli karein ---

if prompt := st.chat_input("Analyze Phase 8 vs Precinct 10..."):
    # ... (baqi search wala code wahi rahega)

    with st.chat_message("assistant"):
        # AI Response
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        
        full_response = completion.choices[0].message.content
        
        # Maxout Logic: Score nikalne ka tarika
        import re
        try:
            # AI ke jawab se "SCORE:85" jaisa text dhoondna
            found_score = re.search(r"SCORE:(\d+)", full_response)
            if found_score:
                new_score = int(found_score.group(1))
                st.session_state.market_score = new_score # Score update ho gaya!
        except:
            st.session_state.market_score = 78 # Default agar AI bhool jaye
            
        st.markdown(full_response)

# --- Sidebar mein Gauge Chart ko update karein ---
if "market_score" not in st.session_state:
    st.session_state.market_score = 78 # Shuruat mein 78

# Gauge Chart mein value ko session_state se connect karein
fig.add_trace(go.Indicator(
    mode = "gauge+number",
    value = st.session_state.market_score, # Ab ye move karega!
    # ... baqi settings wahi
))
