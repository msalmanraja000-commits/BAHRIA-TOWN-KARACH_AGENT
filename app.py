import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import plotly.graph_objects as go

st.markdown("""
    <style>
    /* 1. Global Dark Theme */
    .stApp { 
        background-color: #000000; 
        color: #ffffff !important; 
        font-family: 'Segoe UI', sans-serif; 
    }

    /* 2. Sidebar Force White Text & Black Background */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333;
    }

    /* Making "Elite Analytics" and all Sidebar headers Crystal White */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    /* 3. Chat Messages Styling */
    .stChatMessage { 
        background-color: #111111; 
        border: 0.5px solid #444; 
        border-radius: 8px; 
        padding: 15px; 
    }

    /* 4. Gauge Chart Label Color */
    .js-line { stroke: white !important; }
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
