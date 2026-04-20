import streamlit as st
import requests

st.set_page_config(page_title="Loan Prediction App", layout="centered")

st.title("Loan Approval Prediction")
st.markdown("Fill the details below to predict loan approval")

# --- Input Fields ---
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])

app_income = st.number_input("Applicant Income", min_value=0.0)
coapp_income = st.number_input("Coapplicant Income", min_value=0.0)
loan_amount = st.number_input("Loan Amount", min_value=0.0)
loan_term = st.number_input("Loan Amount Term", min_value=0.0)

credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# --- Button ---
if st.button("Predict Loan Status"):
    
    url = "http://54.242.241.73:8001/lone_prediction"

    data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": app_income,
        "CoapplicantIncome": coapp_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        if result['prediction'] == 1:
            st.success("Loan Approved")
        else:
            st.error("Loan Rejected")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")