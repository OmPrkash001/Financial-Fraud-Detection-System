import pandas as pd
import joblib
import streamlit as st
import os

# Define paths
MODEL_PATH = 'xgb_model.pkl'
ENCODER_PATH = 'encoders.pkl'
SCALER_PATH = 'standard_scaler.pkl'

# Load artifacts
@st.cache_resource
def load_artifacts():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH) or not os.path.exists(SCALER_PATH) or not os.path.exists('feature_names.pkl'):
        return None, None, None, None
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load('feature_names.pkl')
    return model, encoder, scaler, feature_names

model, encoder, scaler, feature_names = load_artifacts()

def main():
    st.title("Financial Fraud Detection System")
    
    if model is None:
        st.error("Model artifacts not found. Please run `train.py` first to generate the model.")
        return

    st.write("Enter transaction details to check for fraud.")

    # Input fields
    amt = st.number_input("Transaction Amount", min_value=0.0)
    category = st.selectbox("Category", ['grocery_pos', 'entertainment', 'shopping_pos', 'misc_pos', 'shopping_net', 'gas_transport', 'misc_net', 'grocery_net', 'food_dining', 'health_fitness', 'kids_pets', 'home', 'personal_care', 'travel'])
    gender = st.selectbox("Gender", ['M', 'F'])
    state = st.text_input("State (e.g., NY, CA)")
    job = st.text_input("Job Title")
    age = st.number_input("Age", min_value=18, max_value=120, value=30)
    hour = st.slider("Hour of Day", 0, 23, 12)
    
    if st.button("Predict"):
        # Preprocess input
        def categorize_hour(h):
            if 0 <= h < 6: return 'Early Morning'
            elif 6 <= h < 12: return 'Morning'
            elif 12 <= h < 18: return 'Afternoon'
            else: return 'Evening'
            
        input_data = pd.DataFrame({
            'amt': [amt],
            'category': [category],
            'gender': [gender],
            'state': [state],
            'job': [job],
            'age': [age],
            'hour': [hour],
            'merchant': ['dummy_merchant'], # Placeholder as merchant might be high cardinality
            'Hour_Category': [categorize_hour(hour)]
        })
        
        # Transform
        try:
            input_encoded = encoder.transform(input_data)
            input_encoded['amt'] = scaler.transform(input_encoded[['amt']])
            
            # Align columns if necessary (BinaryEncoder might create different columns if new categories appear, 
            # but usually it handles unknown categories gracefully if configured, or we assume training data covered them)
            # For simplicity, we assume the encoder handles it or we might need to align with training columns.
            input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)
            
            prediction = model.predict(input_encoded)
            prob = model.predict_proba(input_encoded)[0][1]
            
            if prediction[0] == 1:
                st.error(f"FRAUD DETECTED! (Probability: {prob:.2f})")
            else:
                st.success(f"Transaction is Safe. (Probability: {prob:.2f})")
                
        except Exception as e:
            st.error(f"Error during prediction: {e}")

if __name__ == "__main__":
    main()
