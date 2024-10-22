from typing import Counter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

def get_business_data():
    url = "http://localhost:8000/business/summary"
    response = requests.get(url)
    return response

def get_eco_data():
    url = "http://localhost:8000/eco/summary"
    response = requests.get(url)
    return response

def get_ecoPlus_data():
    url = "http://localhost:8000/ecoPlus/summary"
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
        with col2:
            option = st.selectbox(
                "Analyzer",
                ("None", "Economy Class", "Economy Plus Class", "Business Class"),
            )
    st.markdown("**- Classify Satisfaction, Neutral or Dissatisfaction of passenger based on history data -**")

    if option == "Economy Class":
        res = get_eco_data()
    elif option == "Economy Plus Class":
        res = get_ecoPlus_data()
    elif option == "Business Class":
        res = get_business_data()
    else:
        res = None

    with st.container(border=True):
        if res != None:
            st.markdown("<h3 style='margin-top: 20px; margin-bottom: 70px; text-align: center;'>CDTI Airplane Flight 640</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            if res != None:
                st.image("./assets/AirplaneSeat.png")
        with col2:
            with st.container():
                if res != None:
                    st.success('Analyze succesfully', icon="✅")
                    if option == "Economy Class":
                        st.markdown("### :green[Economy Class]")
                    elif option == "Economy Plus Class":
                        st.markdown("### :blue[Economy Plus Class]")
                    elif option == "Business Class":
                        st.markdown("### :rainbow[Business Class]")
                    df = pd.DataFrame(res.json()['data'])
                    preds = res.json()['preds']
                    feature_importance = res.json()['feature_importance']
                    
                    df_preds = pd.DataFrame(preds)
                    satisfaction_counts = df_preds.value_counts()
                    count_satisfied = satisfaction_counts['satisfied']
                    count_neutral_dissatisfied = satisfaction_counts['neutral or dissatisfied']
                    
                    sa_col1, dis_col2 = st.columns(2)
                    
                    sa_col1.metric(label="Satisfied", value=f"{count_satisfied} 👤", delta="+ 😁")
                    dis_col2.metric(label="Neutral or Dissatisfied", value=f"{count_neutral_dissatisfied} 👤", delta="- 🫤")
                    
                    # Extracting the features with negative importance from the nested structure
                    negative_features = [item['Feature'] for item in feature_importance if item['Importance'] < 0]
                    
                    # Extract base names (ignore numbers after the underscore)
                    base_names = [name.split('_')[0] for name in negative_features]

                    # Count occurrences of base names
                    name_counts = Counter(base_names)
                    print(name_counts)
                    
                    # Get names that appear exactly once
                    unique_names = [name for name, count in name_counts.items() if count > 1]
                    
                    with st.container(border=True):
                        st.markdown("#### Services that need to be developed to enhance passenger satisfaction. 📖")
                        
                        for name in unique_names[0:3]:
                            st.markdown(f"""
                                        - {name}
                                        """)
                        
                    st.markdown("> based on history data")
        
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