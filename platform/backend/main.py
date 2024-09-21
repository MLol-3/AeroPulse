import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI
import joblib
import pandas as pd
import pickle

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
    
    df = pd.DataFrame(data)
    df = df.drop(["id"], axis=1)
    encoder = joblib.load('./utils/encoder.pkl')
    scaler = joblib.load('./utils/scaler.pkl')
    model = joblib.load("./utils/model_lr copy.pkl")
    model2 = pickle.load(open("./utils/model_lr copy.pkl", "rb"))
    
    all_encoded = ['Inflight wifi service', 
                    'Departure/Arrival time convenient', 
                    'Ease of Online booking', 'Gate location', 
                    'Food and drink', 'Online boarding', 'Seat comfort', 
                    'Inflight entertainment', 'On-board service', 
                    'Leg room service', 'Baggage handling', 'Checkin service', 
                    'Inflight service', 'Cleanliness', 'Gender', 'Customer Type', 
                    'Type of Travel', 'Class']
    encoded = encoder.fit_transform(df[all_encoded])

    df_encoded = pd.DataFrame(encoded.toarray(), 
                              columns=encoder.get_feature_names_out(all_encoded))
    
    df_encoded.to_csv('encoded.csv', index=False)
    
    # encoding
    df_encoded = df_encoded.astype(int)
    print(len(list(df_encoded)))
    df_encoded = df_encoded[6:]
    df_drop_dummy = df[6:].drop(all_encoded, axis=1)
    df_final = pd.concat([df_encoded, df_drop_dummy], axis=1)
    
    df_final.to_csv('concat.csv', index=False)
    
    # standardization
    df_scaler = scaler.transform(df_final)
    preds = model2.predict(df_scaler)
    print(preds)

    # Return the data as JSON response
    return {"data": data}