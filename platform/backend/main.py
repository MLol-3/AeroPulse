from sklearn.inspection import permutation_importance
import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI
import joblib
import pandas as pd
import pickle

def transform_pipeline_business(df):
    df = df.drop(["id"], axis=1)
    print(df)
    encoder = pickle.load(open("../../pipelines/encoder_business.pkl", 'rb'))
    # encoder = joblib.load('../../pipelines/encoder_business.pkl')
    model = pickle.load(open("../../pipelines/model_LR_business.pkl", 'rb'))
    scaler = pickle.load(open("../../pipelines/scaler_LR_business.pkl", 'rb'))
    
    all_encoded = ['Inflight wifi service', 
                    'Ease of Online booking', 
                    'Food and drink', 'Online boarding', 
                    'Seat comfort', 'Inflight entertainment', 
                    'On-board service', 'Leg room service', 
                    'Baggage handling', 'Checkin service', 
                    'Inflight service', 'Cleanliness', 
                    'Customer Type', 'Type of Travel', 'Class']
    encoded = encoder.fit_transform(df[all_encoded])

    df_encoded = pd.DataFrame(encoded.toarray(), 
                            columns=encoder.get_feature_names_out(all_encoded))
    # # encoding
    df_encoded = df_encoded.astype(int)
    print(df_encoded.shape)
    # print(len(list(df_encoded)))
    # df_encoded = df_encoded[6:]
    df_drop_dummy = df[6:].drop(all_encoded, axis=1)
    
    df_drop_dummy = df_drop_dummy.drop(["Gender", "Gate location", "Arrival Delay in Minutes", "Departure/Arrival time Convenient"], axis=1)
    print(df_drop_dummy.shape)
    df_drop_dummy_reset = df_drop_dummy.reset_index(drop=True)
    df_encoded_reset = df_encoded.reset_index(drop=True)

    df_final = pd.concat([df_encoded_reset, df_drop_dummy_reset], axis=1)
    print(df_final.shape)
    
    # standardization
    df_scaler = scaler.transform(df_final.iloc[:-6])
    preds = model.predict(df_scaler)
    
    feature_importance = pd.DataFrame({
        'Feature': df_final.columns.tolist(),  # List of feature names
        'Importance': model.coef_[0]  # Coefficients of the logistic regression model
    }).sort_values(by='Importance', ascending=False)
    
    return preds, feature_importance

def transform_pipeline_eco(df):
    df = df.drop(["id"], axis=1)
    print(df)
    encoder = pickle.load(open("../../pipelines/encoder_eco.pkl", 'rb'))
    # encoder = joblib.load('../../pipelines/encoder_business.pkl')
    model = pickle.load(open("../../pipelines/model_LR_eco.pkl", 'rb'))
    scaler = pickle.load(open("../../pipelines/scaler_LR_eco.pkl", 'rb'))
    
    all_encoded = ['Inflight wifi service', 
                    'Ease of Online booking', 
                    'Food and drink', 'Online boarding', 
                    'Seat comfort', 'Inflight entertainment', 
                    'On-board service', 'Leg room service', 
                    'Baggage handling', 'Checkin service', 
                    'Inflight service', 'Cleanliness', 
                    'Customer Type', 'Type of Travel', 'Class']
    encoded = encoder.fit_transform(df[all_encoded])

    df_encoded = pd.DataFrame(encoded.toarray(), 
                            columns=encoder.get_feature_names_out(all_encoded))
    # # encoding
    df_encoded = df_encoded.astype(int)
    print(df_encoded.shape)
    
    # print(len(list(df_encoded)))
    # df_encoded = df_encoded[6:]
    df_drop_dummy = df[6:].drop(all_encoded, axis=1)
    
    df_drop_dummy = df_drop_dummy.drop(["Gender", "Gate location", "Arrival Delay in Minutes", "Departure/Arrival time Convenient"], axis=1)
    print(df_drop_dummy.shape)
    df_drop_dummy_reset = df_drop_dummy.reset_index(drop=True)
    df_encoded_reset = df_encoded.reset_index(drop=True)

    df_final = pd.concat([df_encoded_reset, df_drop_dummy_reset], axis=1)
    df_final.to_csv("eco_encode.csv", index=False)
    
    # standardization
    df_scaler = scaler.transform(df_final.iloc[:-6])
    preds = model.predict(df_scaler)
    
    feature_importance = pd.DataFrame({
        'Feature': df_final.columns.tolist(),  # List of feature names
        'Importance': model.coef_[0]  # Coefficients of the logistic regression model
    }).sort_values(by='Importance', ascending=False)
    
    return preds, feature_importance

def transform_pipeline_ecoPlus(df):
    df = df.drop(["id"], axis=1)
    print(df)
    encoder = pickle.load(open("../../pipelines/encoder_ecoPlus.pkl", 'rb'))
    # encoder = joblib.load('../../pipelines/encoder_business.pkl')
    model = pickle.load(open("../../pipelines/model_LR_ecoPlus.pkl", 'rb'))
    scaler = pickle.load(open("../../pipelines/scaler_LR_ecoPlus.pkl", 'rb'))
    
    all_encoded = ['Inflight wifi service', 
                    'Ease of Online booking', 
                    'Food and drink', 'Online boarding', 
                    'Seat comfort', 'Inflight entertainment', 
                    'On-board service', 'Leg room service', 
                    'Baggage handling', 'Checkin service', 
                    'Inflight service', 'Cleanliness', 
                    'Customer Type', 'Type of Travel', 'Class']
    encoded = encoder.fit_transform(df[all_encoded])

    df_encoded = pd.DataFrame(encoded.toarray(), 
                            columns=encoder.get_feature_names_out(all_encoded))
    # # encoding
    df_encoded = df_encoded.astype(int)
    print(df_encoded.shape)
    
    # print(len(list(df_encoded)))
    # df_encoded = df_encoded[6:]
    df_drop_dummy = df[6:].drop(all_encoded, axis=1)
    
    df_drop_dummy = df_drop_dummy.drop(["Gender", "Gate location", "Arrival Delay in Minutes", "Departure/Arrival time Convenient"], axis=1)
    print(df_drop_dummy.shape)
    df_drop_dummy_reset = df_drop_dummy.reset_index(drop=True)
    df_encoded_reset = df_encoded.reset_index(drop=True)

    df_final = pd.concat([df_encoded_reset, df_drop_dummy_reset], axis=1)
    df_final.to_csv("eco_encode.csv", index=False)
    
    # standardization
    df_scaler = scaler.transform(df_final.iloc[:-6])
    preds = model.predict(df_scaler)
    
    feature_importance = pd.DataFrame({
        'Feature': df_final.columns.tolist(),  # List of feature names
        'Importance': model.coef_[0]  # Coefficients of the logistic regression model
    }).sort_values(by='Importance', ascending=False)
    
    return preds, feature_importance

app = FastAPI()

@app.get("/")
def greetings():
    return {"Greetings": "This is Airline Passenger Satisfaction Data Pipeline API."}

@app.get("/rawdata")
def get_raw_data():
    # Define the scope for Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Load credentials from the service account JSON file
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    
    # Authorize the client using the credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheet by its sheet ID
    sheet_id = "1gbTVFkCh1YYlHVN4HpjYP9eFBgAqVneeWKk0qDcKLOE"
    workbook = client.open_by_key(sheet_id)
    
    # Select the first sheet in the workbook
    sheet = workbook.sheet1
    
    # Fetch all records from the sheet
    data = sheet.get_all_records()
    
    # Return the data as JSON response
    return {"data": data}

@app.get("/business/summary")
def get_business_summary():
    # Define the scope for Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Load credentials from the service account JSON file
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    
    # Authorize the client using the credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheet by its sheet ID
    sheet_id = "1gbTVFkCh1YYlHVN4HpjYP9eFBgAqVneeWKk0qDcKLOE"
    workbook = client.open_by_key(sheet_id)
    
    # Select the first sheet in the workbook
    sheet = workbook.sheet1
    
    # Fetch all records from the sheet
    data = sheet.get_all_records()
    print(data)
    
    df = pd.DataFrame(data)
    preds, feature_importance = transform_pipeline_business(df)
    # Convert to a dictionary (records orientation)
    feature_importance_records = feature_importance.to_dict(orient='records')

    # Return the data as JSON response
    return {"data": data[6:], "preds": preds.tolist(), "feature_importance": feature_importance_records}

@app.get("/eco/summary")
def get_eco_summary():
    # Define the scope for Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Load credentials from the service account JSON file
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    
    # Authorize the client using the credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheet by its sheet ID
    sheet_id = "1gbTVFkCh1YYlHVN4HpjYP9eFBgAqVneeWKk0qDcKLOE"
    workbook = client.open_by_key(sheet_id)
    
    # Select the first sheet in the workbook
    sheet = workbook.get_worksheet(1)
    
    # Fetch all records from the sheet
    data = sheet.get_all_records()
    print(data)
    
    df = pd.DataFrame(data)
    preds, feature_importance = transform_pipeline_eco(df)
    # # Convert to a dictionary (records orientation)
    feature_importance_records = feature_importance.to_dict(orient='records')

    # # Return the data as JSON response
    return {"data": data[6:], "preds": preds.tolist(), "feature_importance": feature_importance_records}

@app.get("/ecoPlus/summary")
def get_eco_summary():
    # Define the scope for Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Load credentials from the service account JSON file
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    
    # Authorize the client using the credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheet by its sheet ID
    sheet_id = "1gbTVFkCh1YYlHVN4HpjYP9eFBgAqVneeWKk0qDcKLOE"
    workbook = client.open_by_key(sheet_id)
    
    # Select the first sheet in the workbook
    sheet = workbook.get_worksheet(2)
    
    # Fetch all records from the sheet
    data = sheet.get_all_records()
    print(data)
    
    df = pd.DataFrame(data)
    preds, feature_importance = transform_pipeline_ecoPlus(df)
    # # Convert to a dictionary (records orientation)
    feature_importance_records = feature_importance.to_dict(orient='records')

    # # Return the data as JSON response
    return {"data": data[6:], "preds": preds.tolist(), "feature_importance": feature_importance_records}