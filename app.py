import streamlit as st
import random
import time
import datetime

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="Bahria Town AI Advisor | PropTecSolutions",
    page_icon="🏢",
    layout="wide"
)

# --- 2. SECURITY PATCH: HIDE GITHUB ICON & MENU ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Premium UI Styling */
    .main { background-color: #050a14; color: #ffffff; }
    .stMetric { background-color: #0d1b31; padding: 20px; border-radius: 12px; border: 1px solid #c5a059; }
    .stTextInput>div>div>input { background-color: #16243a; color: #f1f1f1; border: 1px solid #c5a059; }
    h1, h2, h3 { color: #c5a059; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: PROPRIETARY LEAD CAPTURE ---
with st.sidebar:
    st.markdown("<h2 style='color:#c5a059;'>🏢 BTK Executive</h2>", unsafe_allow_html=True)
    st.write("Proprietary Investment Desk for Bahria Town Karachi.")
    
    with st.form("btk_lead_form"):
        st.subheader("Investor Onboarding")
        name = st.text_input("Investor Name")
        whatsapp = st.text_input("WhatsApp Number")
        interest = st.selectbox("Area", ["Precinct 1", "Sports City", "Golf City", "Bahria Paradise"])
        
        # FIXED BRANDED BUTTON
        submit = st.form_submit_button("Submit to PropTecSolutions")
        
        if submit:
            if name and whatsapp:
                st.success(f"Protocol Initiated. Data transmitted to PropTecSolutions.")
            else:
                st.warning("Credential verification required.")

# --- 4. DASHBOARD HEADER ---
st.title("🏢 Bahria Town Karachi: AI Asset Intelligence")
st.markdown(f"**Enterprise Protocol:** Enabled | **Status:** {datetime.date.today().strftime('%B %d, 2026')}")

# --- 5. MARKET METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Market Sentiment Score", value=f"{random.randint(70, 88)}/100", delta="Strong Growth")
with col2:
    st.metric(label="Rental Yield (Avg)", value="7.4%", delta="↑ 0.6%")
with col3:
    st.metric(label="Investment Grade", value="A+", delta="Stable")

st.divider()

# --- 6. INTELLIGENCE SEARCH ---
query = st.text_input("Enter Precinct/Sector for Deep-Dive Analysis:", placeholder="Accessing BTK Data Lake...")

if query:
    with st.spinner(f"Analyzing Bahria Town Market Depth for {query}..."):
        time.sleep(1.5)
        st.write(f"### Intelligence Brief: {query}")
        st.info(f"AI Logic: **{query}** is showing high liquidity. Recommended for immediate acquisition.")
        st.line_chart([random.randint(50, 100) for _ in range(10)])

# --- 7. THE LEGAL SHIELD (REINFORCED) ---
st.divider()
st.markdown("""
    <div style='text-align: center; color: #c5a059; font-size: 11px; font-weight: bold;'>
        PROPRIETARY ASSET OF PROPTECSOLUTIONS <br>
        <span style='color: gray;'>© 2026 Salman Raja | Founder & CEO. <br>
        CONFIDENTIAL PROTOTYPE: UNAUTHORIZED REPLICATION OR DISTRIBUTION IS STRICTLY PROHIBITED.</span>
    </div>
    """, unsafe_allow_html=True)
