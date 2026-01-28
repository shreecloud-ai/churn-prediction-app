from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Dict

app = FastAPI(title="Telco Customer Churn Prediction API")

# Load the trained model (from the joblib file)
MODEL_PATH = "../models/churn_pipeline_rf.joblib"
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Define the input data structure (must match your training features)
class CustomerInput(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict", response_model=Dict)
async def predict_churn(customer: CustomerInput):
    try:
        # Convert input to DataFrame (single row)
        input_df = pd.DataFrame([customer.dict()])

        # Make prediction
        prob = model.predict_proba(input_df)[0][1]  # probability of churn (class 1)
        prediction = int(model.predict(input_df)[0])  # 0 or 1

        return {
            "churn_probability": round(float(prob), 4),
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "risk_level": "High" if prob > 0.5 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}