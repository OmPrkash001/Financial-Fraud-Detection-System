import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
# Serving static files from the 'public' folder one level up
app = Flask(__name__, static_folder='../public', static_url_path='')
CORS(app)  # Enable Cross-Origin Resource Sharing for local testing

@app.route('/')
def home():
    return app.send_static_file('index.html')

# Load artifacts (function-level caching to avoid reloading on every request in generic Flask, 
# though Cloud Functions reuses the instance)
model = None
encoder = None
scaler = None
feature_names = None

def load_artifacts():
    global model, encoder, scaler, feature_names
    if model is None:
        model = joblib.load('xgb_model.pkl')
        encoder = joblib.load('encoders.pkl')
        scaler = joblib.load('standard_scaler.pkl')
        feature_names = joblib.load('feature_names.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        load_artifacts()
        
        data = request.get_json()
        
        # Preprocess input (calculate derived features)
        # Note: 'age' and 'hour' are direct inputs now, matching app.py logic
        
        def categorize_hour(h):
            if 0 <= h < 6: return 'Early Morning'
            elif 6 <= h < 12: return 'Morning'
            elif 12 <= h < 18: return 'Afternoon'
            else: return 'Evening'

        input_df = pd.DataFrame([data])
        
        # Ensure derived feature exists
        if 'Hour_Category' not in input_df.columns and 'hour' in input_df.columns:
             input_df['Hour_Category'] = input_df['hour'].apply(categorize_hour)
        
        # Add dummy merchant if missing (since we used it in training)
        if 'merchant' not in input_df.columns:
            input_df['merchant'] = 'dummy_merchant'

        # Transform
        input_encoded = encoder.transform(input_df)
        input_encoded['amt'] = scaler.transform(input_encoded[['amt']])
        
        # Reorder columns to match training
        input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)
        
        # Predict
        prediction = model.predict(input_encoded)[0]
        probability = model.predict_proba(input_encoded)[0][1]
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == "__main__":
    # For local testing
    app.run(debug=True, port=5000)
