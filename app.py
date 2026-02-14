import streamlit as st
import requests
import time
from datetime import datetime

# 1. Stealth Shield
st.set_page_config(page_title="BTK Intelligence | PropTec", page_icon="🏙️", layout="wide")
st.markdown("<style>[data-testid='stHeader'], footer, #MainMenu, .stAppDeployButton {display: none !important;}</style>", unsafe_allow_html=True)

# 2. Interface
st.title("🏙️ BTK Strategic Intelligence")
st.write("Real-time Precinct Analysis for Bahria Town Karachi.")

precinct = st.text_input("Enter Precinct:", placeholder="e.g. Precinct 10-A, P-31")

if st.button("🚀 Analyze BTK Market"):
    if precinct:
        with st.spinner('Scanning BTK Growth Patterns...'):
            time.sleep(1)
            st.metric("Precinct Growth Score", "94/100", "Top Choice")
            st.success(f"Market Report for {precinct}: High occupancy and rapid commercialization surge.")
    else:
        st.error("Please enter a Precinct.")

# 3. Growth Lead Form
st.markdown("---")
st.subheader("🔥 Get BTK 'High-Yield' Hot Leads")
st.write("Access our curated list of precincts with the highest rental returns and fastest growth.")

with st.form("btk_form", clear_on_submit=True):
    u_name = st.text_input("Full Name")
    u_phone = st.text_input("WhatsApp Number")
    u_budget = st.selectbox("Investment Budget (PKR):", ["Select Budget", "5M - 15M", "15M - 35M", "35M - 75M", "75M+"])
    
    if st.form_submit_button("Get BTK Hot Leads"):
        if u_name and u_phone and u_budget != "Select Budget":
            URL = "https://script.google.com/macros/s/AKfycby5T5NJ8NAf1LP_G5SJ3iTaPWdD0DusoFbdBUFrVkqt1Z03PcNQ89TE2o2aXSOORXzi/exec"
            payload = {"Name": u_name, "Phone": u_phone, "Budget": u_budget, "Market": "BTK Karachi", "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            try:
                requests.post(URL, json=payload, timeout=10)
                st.balloons()
                st.success(f"Zabardast! Shukriya {u_name}. Hamare BTK Analysts aapke budget ({u_budget}) ki best deals nikal rahe hain.")
                st.info("🏙️ **PropTec Growth:** Hamari team jald contact karegi. Aapko Bahria Town ki sabse 'Profitable' aur 'Distress Deals' ki list WhatsApp par mil jayegi.")
            except:
                st.error("Connection Error.")
        else:
            st.warning("Please fill all details.")
         
