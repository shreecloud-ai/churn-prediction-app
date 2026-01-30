import streamlit as st
import requests
import pandas as pd
from PIL import Image
import os

# --- Config ---
st.set_page_config(page_title="Telco Churn Predictor", layout="wide")

API_URL = "http://127.0.0.1:8000/predict"   # change to deployed URL later

# --- Title & Description ---
st.title("Customer Churn Prediction App")
st.markdown("""
Enter customer details to see the predicted **churn probability** and risk level.
Powered by Random Forest model trained on Telco data.
""")

# --- Sidebar with info ---
with st.sidebar:
    st.header("About")
    st.markdown("This app uses a saved scikit-learn pipeline to predict churn.")
    st.markdown("Model ROC AUC ~0.83–0.85")
    st.image("notebooks/plots/tenure_vs_churn.png", caption="Tenure vs Churn", use_column_width=True)

# --- Input Form ---
with st.form("customer_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=12)
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

    with col2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=70.0, step=0.1)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=9000.0, value=1000.0, step=1.0)

    submitted = st.form_submit_button("Predict Churn")

# --- Prediction logic ---
if submitted:
    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # raise error if not 200
        result = response.json()

        st.success(f"**Churn Probability:** {result['churn_probability'] * 100:.1f}%")
        st.info(f"**Prediction:** {result['churn_prediction']} ({result['risk_level']} risk)")

        # Show some plots
        col1, col2 = st.columns(2)
        with col1:
            st.image("notebooks/plots/tenure_vs_churn.png", caption="Tenure vs Churn")
        with col2:
            st.image("notebooks/plots/monthly_charges_vs_churn.png", caption="Monthly Charges vs Churn")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")