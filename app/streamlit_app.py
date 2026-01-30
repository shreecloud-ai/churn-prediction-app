import streamlit as st
import requests
import os

# ────────────────────────────────────────────────
#  Page config & basic setup
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Predictor",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint (change when deployed)
API_URL = "http://127.0.0.1:8000/predict"
# API_URL = "https://your-app-name.onrender.com/predict"  # after deployment

# ────────────────────────────────────────────────
#  Helper functions
# ────────────────────────────────────────────────
def load_image(path: str) -> str | None:
    """Safe image loader with fallback"""
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
    if os.path.exists(full_path):
        return full_path
    return None

def get_rule_based_explanation(prob: float) -> str:
    """Simple fallback explanation when LLM is unavailable"""
    if prob > 0.7:
        return (
            "High churn risk detected. This customer likely has short tenure, "
            "high monthly charges and/or a flexible month-to-month contract — "
            "common signs of dissatisfaction. A loyalty discount or personalized "
            "offer could significantly improve retention chances."
        )
    elif prob > 0.4:
        return (
            "Moderate churn risk. There are some concerning signals such as "
            "shorter tenure or above-average billing. A proactive check-in "
            "or small incentive might prevent this customer from leaving."
        )
    else:
        return (
            "Low churn risk. This customer appears stable — probably longer "
            "tenure and reasonable charges. Continuing to deliver good service "
            "should keep them satisfied and loyal."
        )

# ────────────────────────────────────────────────
#  Sidebar
# ────────────────────────────────────────────────
with st.sidebar:
    st.title("Telco Churn Predictor")
    st.markdown("**Model:** Random Forest (~0.83–0.85 ROC AUC)")
    st.markdown("**Goal:** Identify customers at risk of leaving")

    st.divider()
    st.subheader("Key Insights")

    tenure_img = load_image("notebooks/plots/tenure_vs_churn.png")
    if tenure_img:
        st.image(tenure_img, caption="Shorter tenure → higher churn")
    else:
        st.caption("Tenure plot not found")

    charges_img = load_image("notebooks/plots/monthly_charges_vs_churn.png")
    if charges_img:
        st.image(charges_img, caption="Higher charges → higher churn")
    else:
        st.caption("Monthly charges plot not found")

# ────────────────────────────────────────────────
#  Main content – Tabs
# ────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Make Prediction", "ℹ️ About the Model"])

# ── Tab 1: Prediction ────────────────────────────────────────
with tab1:
    st.header("Predict Customer Churn")

    with st.form("prediction_form"):
        st.subheader("Customer Information")

        col1, col2 = st.columns([1, 1])

        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"], index=0)
            senior = st.selectbox("Senior Citizen", [0, 1], index=0)
            partner = st.selectbox("Partner", ["Yes", "No"], index=0)
            dependents = st.selectbox("Dependents", ["Yes", "No"], index=0)
            tenure = st.slider("Tenure (months)", 0, 72, 12)

        with col2:
            phone = st.selectbox("Phone Service", ["Yes", "No"], index=0)
            multiple_lines = st.selectbox(
                "Multiple Lines", ["Yes", "No", "No phone service"], index=0
            )
            internet = st.selectbox(
                "Internet Service", ["DSL", "Fiber optic", "No"], index=0
            )
            contract = st.selectbox(
                "Contract", ["Month-to-month", "One year", "Two year"], index=0
            )
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"], index=0)
            payment = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
                index=0,
            )

        # Second row – service add-ons
        st.subheader("Internet Add-ons (if applicable)")
        col3, col4, col5 = st.columns(3)

        with col3:
            online_security = st.selectbox(
                "Online Security", ["Yes", "No", "No internet service"], index=2
            )
            online_backup = st.selectbox(
                "Online Backup", ["Yes", "No", "No internet service"], index=2
            )

        with col4:
            device_protection = st.selectbox(
                "Device Protection", ["Yes", "No", "No internet service"], index=2
            )
            tech_support = st.selectbox(
                "Tech Support", ["Yes", "No", "No internet service"], index=2
            )

        with col5:
            streaming_tv = st.selectbox(
                "Streaming TV", ["Yes", "No", "No internet service"], index=2
            )
            streaming_movies = st.selectbox(
                "Streaming Movies", ["Yes", "No", "No internet service"], index=2
            )

        # Charges
        st.subheader("Billing")
        col6, col7 = st.columns(2)
        with col6:
            monthly_charges = st.number_input(
                "Monthly Charges (₹)", 0.0, 200.0, 70.0, step=0.5
            )
        with col7:
            total_charges = st.number_input(
                "Total Charges (₹)", 0.0, 10000.0, 1000.0, step=10.0
            )

        submitted = st.form_submit_button("Calculate Churn Risk", type="primary", use_container_width=True)

    # ── Prediction logic ────────────────────────────────────────
    if submitted:
        with st.spinner("Analyzing customer…"):
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
                "TotalCharges": total_charges,
            }

            try:
                r = requests.post(API_URL, json=payload, timeout=10)
                r.raise_for_status()
                data = r.json()

                prob = data.get("churn_probability", 0)
                prediction = data.get("churn_prediction", "Unknown")
                risk = data.get("risk_level", "Unknown")

                # Result cards
                col_a, col_b = st.columns([1, 2])

                with col_a:
                    st.metric("Churn Probability", f"{prob*100:.1f}%")

                    if prediction == "Yes":
                        st.error(f"**Likely to churn**  ({risk} risk)")
                    else:
                        st.success(f"**Likely to stay**  ({risk} risk)")

                with col_b:
                    st.markdown("#### Interpretation")
                    st.info(get_rule_based_explanation(prob))

            except requests.exceptions.RequestException as e:
                st.error(f"Cannot reach prediction server\n{e}\n\nIs FastAPI running on port 8000?")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ────────────────────────────────────────────────
#  Tab 2: About
# ────────────────────────────────────────────────
with tab2:
    st.header("About this App")
    st.markdown("""
    This is an end-to-end demonstration project built to showcase:

    - Data exploration & visualization (pandas, seaborn, matplotlib)
    - Machine learning pipeline (scikit-learn, Random Forest)
    - Model serving (FastAPI)
    - Interactive web app (Streamlit)

    **Dataset:** Telco Customer Churn (Kaggle)  
    **Goal:** Predict which customers are likely to leave and why.

    Created in Pune, Maharashtra – January 2026
    """)

    st.markdown("---")
    st.caption("Built for learning MLOps & deployment")