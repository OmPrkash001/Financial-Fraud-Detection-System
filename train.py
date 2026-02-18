import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import category_encoders as ce

# Define paths
TRAIN_DATA_PATH = 'train_data.csv'
TEST_DATA_PATH = 'test_data.csv'
MODEL_PATH = 'xgb_model.pkl'
ENCODER_PATH = 'encoders.pkl'
SCALER_PATH = 'standard_scaler.pkl'

def load_data():
    if not os.path.exists(TRAIN_DATA_PATH) or not os.path.exists(TEST_DATA_PATH):
        print(f"Error: Data files not found. Please ensure '{TRAIN_DATA_PATH}' and '{TEST_DATA_PATH}' are in the current directory.")
        return None, None
    
    print("Loading data...")
    dftrain = pd.read_csv(TRAIN_DATA_PATH)
    dftest = pd.read_csv(TEST_DATA_PATH)
    return dftrain, dftest

def preprocess_data(dftrain, dftest):
    print("Preprocessing data...")
    dftotal = pd.concat([dftrain, dftest], ignore_index=True)
    
    # Sampling to balance dataset (simplified from notebook)
    dfFraud = dftotal[dftotal['is_fraud'] == 1]
    remaining_rows = 100000 - len(dfFraud)
    filteredNotFraud = dftotal[dftotal['is_fraud'] == 0]
    
    if len(filteredNotFraud) < remaining_rows:
        print("Warning: Not enough non-fraud data to reach 100k rows. Using all available.")
        dfNFraud = filteredNotFraud
    else:
        dfNFraud = filteredNotFraud.sample(n=remaining_rows, random_state=42)
        
    dataExtracted = pd.concat([dfNFraud, dfFraud], ignore_index=True)
    
    # Feature Engineering (simplified)
    dataExtracted['trans_date_trans_time'] = pd.to_datetime(dataExtracted['trans_date_trans_time'])
    dataExtracted['dob'] = pd.to_datetime(dataExtracted['dob'])
    dataExtracted['hour'] = dataExtracted['trans_date_trans_time'].dt.hour
    dataExtracted['age'] = (dataExtracted['trans_date_trans_time'] - dataExtracted['dob']).dt.days // 365
    
    # Define categories
    def categorize_hour(hour):
        if 0 <= hour < 6: return 'Early Morning'
        elif 6 <= hour < 12: return 'Morning'
        elif 12 <= hour < 18: return 'Afternoon'
        else: return 'Evening'

    dataExtracted['Hour_Category'] = dataExtracted['hour'].apply(categorize_hour)
    
    # Drop unnecessary columns
    drop_cols = ['Unnamed: 0', 'trans_date_trans_time', 'cc_num', 'first', 'last', 'street', 'city', 'zip', 'dob', 'trans_num', 'unix_time', 'merch_lat', 'merch_long', 'lat', 'long', 'city_pop']
    dataExtracted = dataExtracted.drop(columns=[col for col in drop_cols if col in dataExtracted.columns], errors='ignore')
    
    return dataExtracted

def train_model(data):
    print("Training model...")
    X = data.drop('is_fraud', axis=1)
    y = data['is_fraud']
    
    # Encoding
    categorical_cols = ['merchant', 'category', 'gender', 'state', 'job', 'Hour_Category']
    # Note: In a real scenario, we should fit on train and transform on test. 
    # Here we are following the notebook's approach of processing the extracted dataset.
    
    encoder = ce.BinaryEncoder(cols=categorical_cols)
    X_encoded = encoder.fit_transform(X)
    
    # Scaling
    scaler = StandardScaler()
    X_encoded['amt'] = scaler.fit_transform(X_encoded[['amt']])
    
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    # Save artifacts
    print("Saving artifacts...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(X_encoded.columns.tolist(), 'feature_names.pkl')
    print("Done.")

if __name__ == "__main__":
    dftrain, dftest = load_data()
    if dftrain is not None:
        data = preprocess_data(dftrain, dftest)
        train_model(data)
