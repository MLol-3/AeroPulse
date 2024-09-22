from sklearn.inspection import permutation_importance
import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI
import joblib
import pandas as pd
import pickle

def transform_pipeline(df):
    df = df.drop(["id"], axis=1)
    print(df)
    encoder = pickle.load(open("../../pipelines/encoder_business.pkl", 'rb'))
    # encoder = joblib.load('../../pipelines/encoder_business.pkl')
    model = pickle.load(open("../../pipelines/model_KNN_business.pkl", 'rb'))
    scaler = pickle.load(open("../../pipelines/scaler.pkl", 'rb'))
    
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
    # print(df_final.iloc[:-6]["Departure/Arrival time Convenient"])
    df_final.iloc[:-6].to_csv("hi.csv", index=False)
    print(df_final.iloc[:-6].shape)
    # # # standardization
    df_scaler = scaler.transform(df_final.iloc[:-6])
    preds = model.predict(df_scaler)
    
    # Calculate permutation importance on the test set
    result = permutation_importance(model, df_scaler, y_test, n_repeats=10, random_state=42)

    # Create a dataframe with feature importance scores
    feature_importance = pd.DataFrame({
        'Feature': df_drop_dummy.columns,
        'Importance': result.importances_mean
    }).sort_values(by='Importance', ascending=False)
    
    return preds


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

    # Return the data as JSON response
    return {"data": data[6:], "preds": preds.tolist()}