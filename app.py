import streamlit as st
import requests
import time
from datetime import datetime

# --- 🛡️ STEALTH & COPYRIGHT SECURITY ---
st.set_page_config(page_title="BTK Intelligence | PropTec", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {display: none !important; visibility: hidden !important;}
    .viewerBadge_container__1QSob { display: none !important; }
    .stApp { background-color: #0E1117; }
    .custom-footer {
        position: fixed; left: 0; bottom: 0; width: 100%; 
        background-color: #161B22; color: #FFD700; 
        text-align: center; padding: 10px; font-size: 13px; 
        border-top: 2px solid #FFD700; z-index: 999;
    }
    </style>
    <div class="custom-footer">© 2026 PropTecSolutions | BTK AI Strategic Framework | Founder: Salman Raja</div>
    """, unsafe_allow_html=True)

# --- 📊 CORE INTERFACE ---
st.title("🏙️ BTK Strategic Intelligence")
st.write("Real-time Precinct Analysis for Bahria Town Karachi.")

precinct = st.text_input("Enter Precinct (e.g. Precinct 10-A, P-31):", placeholder="Analyze precinct...")

if st.button("🚀 Analyze BTK Market"):
    if precinct:
        with st.spinner('Scanning BTK Growth Patterns...'):
            time.sleep(1)
            st.metric("BTK Growth Score", "94/100", "Top Choice")
            st.success(f"Market Report for {precinct} generated successfully!")
    else:
        st.error("Please enter a Precinct.")

# --- 📩 MAX-OUT LEAD FORM (BUDGET + HOOK) ---
st.markdown("---")
with st.form("btk_lead_form", clear_on_submit=True):
    st.subheader("🔥 Get BTK 'High-Yield' Hot Leads")
    st.write("Receive under-market distress deals directly on your WhatsApp.")
    
    u_name = st.text_input("Full Name")
    u_phone = st.text_input("WhatsApp Number")
    u_budget = st.selectbox("Your Investment Budget:", [
        "Select Budget", "5M - 15M", "15M - 35M", "35M - 75M", "75M+"
    ])
    
    submit_btn = st.form_submit_button("Get VIP Access 🚀")
    
    if submit_btn:
        if u_name and u_phone and u_budget != "Select Budget":
            # --- APKA NAYA URL YAHAN DAL DIYA HAI ---
            URL = "https://script.google.com/macros/s/AKfycby1ZemyjAZGkOsJSQ0n_N5CzJ565xVzs_ze8xEgXIlu9yzhEGRb8seO8-HYjxeoZOCF/exec"
            
            payload = {
                "Name": u_name,
                "Phone": u_phone,
                "Budget": u_budget,
                "Market": "BTK Karachi",
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
                # Sending data to sheet
                response = requests.post(URL, json=payload, timeout=10)
                st.balloons()
                st.success(f"Zabardast! Shukriya {u_name}. Hamare BTK Analysts aapka budget ({u_budget}) analyze kar rahe hain.")
                st.info("🏙️ **PropTec Growth:** Hamari team jald contact karegi. Aapko Bahria Town ki sabse 'Profitable' deals WhatsApp par mil jayengi.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            st.warning("Please fill all details correctly.")
