import streamlit as st
from groq import Groq
from tavily import TavilyClient
import plotly.graph_objects as go
import re

# 1. Page Config & Elite Styling
st.set_page_config(page_title="Karachi Enterprise Advisory", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #333; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #111111; border: 0.5px solid #444; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Session State Initialization
if "market_score" not in st.session_state:
    st.session_state.market_score = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Secure Keys
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

# 4. Sidebar: Market Intelligence Gauge
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/combo-chart.png")
    st.title("Elite Analytics")
    sector = st.selectbox("Market Focus:", ["DHA Karachi", "Bahria Town Karachi", "Karachi General"])
    
    st.markdown("---")
    st.subheader("Market Confidence Score")
    
    # Custom Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.market_score,
        number = {'font': {'color': "white", 'size': 60}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#00ffcc" if st.session_state.market_score > 0 else "#333"},
            'bgcolor': "#111111",
            'bordercolor': "#ffffff", 'borderwidth': 1
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)
    
    status_text = "Live Sentiment: " + str(st.session_state.market_score) + "%" if st.session_state.market_score > 0 else "Status: Waiting for Analysis"
    st.info(status_text)

# 5. Main Advisor Interface
st.title("🏛️ Karachi Enterprise Advisory")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Analyze Phase 8 or Precinct 10..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Fetching Deep Market Insights...", expanded=False):
            search_res = tavily.search(query=f"latest property rates {sector} {prompt} Karachi Feb 2026", search_depth="advanced")
            intel = "\n".join([r['content'] for r in search_res['results']])
        
        system_msg = f"""
        Identity: Senior Real Estate Strategist. Data: {intel}.
        Provide a professional corporate analysis. Use tables for prices.
        CRITICAL: At the end, you MUST write exactly: INTERNAL_SCORE: [number]
        Example: INTERNAL_SCORE: 85
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        
        full_text = completion.choices[0].message.content
        
        # --- The Ultimate "Cleaner" Logic ---
        score_val = 0
        score_match = re.search(r"INTERNAL_SCORE:\s*(\d+)", full_text)
        
        if score_match:
            score_val = int(score_match.group(1))
            # Score ko session mein daal kar chat se mita dena
            st.session_state.market_score = score_val
            clean_text = re.sub(r"INTERNAL_SCORE:\s*\d+", "", full_text).strip()
        else:
            clean_text = full_text

        st.markdown(clean_text)
        st.session_state.messages.append({"role": "assistant", "content": clean_text})
        
        # Ab poora page refresh karein taake meter upar jaye
        st.rerun()
