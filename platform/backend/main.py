import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI
import joblib
import pandas as pd
import pickle

def transform_pipeline(df):
    df = df.drop(["id"], axis=1)
    encoder = pickle.load(open("../../pipelines/encoder_business.pkl", 'rb'))
    # encoder = joblib.load('../../pipelines/encoder_business.pkl')
    scaler = joblib.load('../../pipelines/scaler.pkl')
    model = joblib.load("../../pipelines/model_KNN_business.pkl")
    
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
    # encoding
    df_encoded = df_encoded.astype(int)
    df_encoded.to_csv("test.csv", index=False)
    # print(len(list(df_encoded)))
    # df_encoded = df_encoded[6:]
    # df_drop_dummy = df[6:].drop(all_encoded, axis=1)
    # df_final = pd.concat([df_encoded, df_drop_dummy], axis=1)
    # # standardization
    # df_scaler = scaler.transform(df_final)
    # preds = model.predict(df_scaler)
    # print(preds)
    
    # return preds


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

@app.get("/summary")
def get_summary():
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
    preds = transform_pipeline(df)
    
    print(df)
    

    # Return the data as JSON response
    return {"data": df}