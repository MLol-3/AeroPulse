import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import gspread
# from google.oauth2.service_account import Credentials
import requests

def getRawData():
    url = "http://localhost:8000/summary"
    response = requests.get(url)
    return response

if __name__ == "__main__":
    
    st.set_page_config(layout='wide', page_title="AeroPulse Visualization", page_icon="✈️")
    
    # Create a container
    with st.container():
        # Create two columns
        col1, col2 = st.columns([6, 1])  # Adjust the width ratio to create space between the columns
        with col1:
            st.title("AeroPulse ✈️")
            st.markdown("**- Classify Satisfaction, Neutral or Dissatisfaction of passenger based on history data -**")
        with col2:
            st.write("")
            if st.button("Summarize The Flight 🧑🏻‍✈️", type="primary"):
                res = getRawData()
            else:
                res = None
        
        st.markdown(
            """
            <style>
            .stTabs [role="tablist"] {
                margin-top: 30px; /* Adjust the value to change the margin */
            }
            </style>
            """,
            unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 20px; margin-bottom: 70px; text-align: center;'>US Airplane Flight 123</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if res != None:
                st.image("./assets/AirplaneSeat.png")
        with col2:
            with st.container():
                if res != None:
                    df = pd.DataFrame(res.json()['data'])
                    preds = res.json()['preds']
                    
                    df_preds = pd.DataFrame(preds)
                    satisfaction_counts = df_preds.value_counts()
                    count_satisfied = satisfaction_counts['satisfied']
                    count_neutral_dissatisfied = satisfaction_counts['neutral or dissatisfied']
                    
                    col1, col2 = st.columns(2)
                    
                    col1.metric(label="Satisfied", value=f"{count_satisfied} 👤", delta="+ 😁")
                    col2.metric(label="Neutral or Dissatisfied", value=f"{count_neutral_dissatisfied} 👤", delta="- 🫤")
        with col3:
            pass
        
        st.markdown("<h3 style='margin-bottom: 20px; text-align: center;'></h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["View Raw Data", "Manual Classify"])
    
    with tab1:
        with st.container():
            if res != None:
                df = pd.DataFrame(res.json()['data'])
                st.dataframe(df) 
            else:
                st.markdown("Waiting for data...")
    with tab2:
        pass