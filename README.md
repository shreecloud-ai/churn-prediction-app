# Telco Customer Churn Prediction Web App

End-to-end machine learning project to predict which telecom customers are likely to churn (leave the service) so the company can offer retention incentives.

Built with Python, scikit-learn, FastAPI, Streamlit, and deployed on Render.com.

## Problem Statement

Customer churn is a major revenue risk in the telecom industry.
This project predicts the probability of a customer churning so
business teams can proactively offer retention incentives.

## Model Performance

- Algorithm: Random Forest Classifier
- Evaluation Metric: ROC-AUC
- ROC-AUC Score: 0.84
- Accuracy: 0.80

The model was trained using cross-validation and class imbalance
was handled during training.

## Live Demo

- **Interactive Web App** (Streamlit frontend):  
  [https://telco-churn-app-x0r2.onrender.com](https://telco-churn-app-x0r2.onrender.com))  
  *(First load may take 30–90 seconds due to free tier spin-up)*

- **API Documentation** (FastAPI Swagger UI):  
  [[https://telco-churn-api-xxx.onrender.com/docs](https://churn-api-toas.onrender.com/docs)  
  (replace xxx with your actual API service name)

## Features

- Interactive form to input customer details (tenure, charges, contract, services, etc.)
- Real-time churn probability (0–100%) + risk level (Low/High)
- Simple rule-based natural language explanation of churn risk
- EDA insights: graphs for tenure vs churn and monthly charges vs churn
- Backend served via FastAPI REST API
- Containerized with Docker & docker-compose for local development
- Deployed on Render.com (free tier)

## Tech Stack

- **Data & ML**: Python, pandas, scikit-learn (Random Forest), joblib
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **Containerization**: Docker + docker-compose
- **Deployment**: Render.com (Docker runtime)
- **Visualization**: Matplotlib, Seaborn

## Note
"First load may take 30–120 seconds due to free tier spin-up"

## Project Structure
churn-prediction-app/
├── app/
│   ├── main.py               # FastAPI backend
│   └── streamlit_app.py      # Streamlit frontend
├── notebooks/
│   ├── 01_eda.ipynb          # Exploratory Data Analysis
│   └── 02_model_training.ipynb # Model training & saving
├── models/
│   └── churn_pipeline_rf.joblib  # Trained model
├── plots/                    # Saved EDA visualizations
├── Dockerfile                # For Streamlit service
├── Dockerfile.api            # For FastAPI service
├── docker-compose.yml        # Local multi-service run
├── requirements.txt          # Dependencies
└── README.md

## Future Improvements

- Replace rule-based explanations with SHAP
- Add CI/CD pipeline
- Add user authentication
- Deploy using paid instance for faster cold starts
## 🚀 Local Setup & Run

### Using pip (recommended for development)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/churn-prediction-app.git
cd churn-prediction-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run API (terminal 1)
cd app
uvicorn main:app --reload

# 4. Run Streamlit (terminal 2)
streamlit run app/streamlit_app.py
Open:

API docs → http://127.0.0.1:8000/docs
Streamlit app → http://localhost:8501

Using Docker (recommended for consistency)
Bashdocker compose up --build
Open:

API docs → http://localhost:8000/docs
Streamlit app → http://localhost:8501



