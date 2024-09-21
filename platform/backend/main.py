import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI

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