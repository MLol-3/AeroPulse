import gspread
from google.oauth2.service_account import Credentials
from typing import Union
from fastapi import FastAPI
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

app = FastAPI()

@app.get("/")
def greetings():
    return {"Greetings": "This is Airline Passenger Satisfaction Data Pipeline API."}

@app.get("/data/summery")
def data_pipeline():
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
    
    # ----------------------------------------------------------------------------------
    
    df = pd.DataFrame(data)
    df_cleaned = df.dropna()
    df_cleaned = df_cleaned.drop(['id'],axis=1).reset_index(drop=True)
    
    encoded_need=[]
    for i in df_cleaned.columns:
        if df_cleaned[i].dtype=='object':
            print(f"Unique values of '{i}' is {df_cleaned[i].unique()}")
            encoded_need.append(i)
        print("Categorical values exist in the columns : ",encoded_need)
        encoded_need = encoded_need[:-1]
        print(encoded_need)
    
    max_values = df_cleaned.max()

    columns_with_max_5 = max_values[max_values == 5].index.tolist()
    encoded_all = columns_with_max_5 + encoded_need

    encoder = OneHotEncoder()

    encoded_object = encoder.fit_transform(df_cleaned[encoded_need])

    df_encoded_object = pd.DataFrame(encoded_object.toarray(), columns=encoder.get_feature_names_out(encoded_need))
    df_encoded_object = df_encoded_object.astype(int)
    
    encoder_ob = OneHotEncoder()

    encoded = encoder_ob.fit_transform(df_cleaned[encoded_all])

    df_encoded = pd.DataFrame(encoded.toarray(), columns=encoder_ob.get_feature_names_out(encoded_all))
    df_encoded = df_encoded.astype(int)

    df_drop_dummy = df_cleaned.drop(encoded_all, axis=1)
    
    df_final = pd.concat([df_encoded, df_drop_dummy], axis=1)
    
    # Assuming 'target_column' is the name of your target column
    target_column = 'satisfaction'
    features = df_final.drop(columns=[target_column])
    target = df_final[target_column]

    # Initialize and fit the scaler
    scaler = StandardScaler()
    features_scaled = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)

    # Combine the scaled features with the target column
    df_transformed = pd.concat([features_scaled, target.reset_index(drop=True)], axis=1)
    
    X = df_transformed.drop(["satisfaction"], axis=1)
    y = df_transformed["satisfaction"]

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
    print(f"Shape of training set is : {X_train.shape} and test set is :{X_test.shape}" )


    # create logistic regression model and fit to training data
    model_lr = LogisticRegression()
    model_lr.fit(X_train, y_train)

    y_pred_lr=model_lr.predict(X_test)
    print(f"Prediction result: {y_pred_lr}")
    score=accuracy_score(y_test,y_pred_lr)
    print(score)

    # see confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred_lr)
    print(conf_matrix)
    # ----------------------------------------------------------------------------------
    
    # Return the data as JSON response
    return {"data": data, "score": score}