# streamlit_app.py
import streamlit as st
import requests
import json

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="Early Identification for Students",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Machine Learning–Based Early Identification of At-Risk Students")
st.markdown(
    "This application predicts whether a student is **academically at risk** "
    "based on demographic, family, and academic attributes."
)

# -----------------------
# API Configuration
# -----------------------
API_URL = "http://127.0.0.1:8001/predict"
st.text(f"POST → {API_URL}")  # Display as text to avoid 'Method Not Allowed' on click

st.divider()

# -----------------------
# Student Information
# -----------------------
st.subheader("📘 Student Information")

col1, col2 = st.columns(2)

with col1:
    school = st.selectbox("School", ["GP", "MS"], index=0)
    sex = st.selectbox("Gender", ["F", "M"], index=0)
    age = st.number_input("Age", min_value=0, max_value=120, value=17, step=1)

with col2:
    address = st.selectbox("Residential Area", ["U", "R"], index=0)
    subject = st.selectbox("Subject", ["math", "portuguese"], index=0)

st.divider()

# -----------------------
# Family Background
# -----------------------
st.subheader("🏠 Family Background")

col3, col4 = st.columns(2)

with col3:
    famsize = st.selectbox("Family Size", ["LE3", "GT3"], index=1)
    Pstatus = st.selectbox("Parental Cohabitation Status", ["T", "A"], index=0)

with col4:
    Medu = st.number_input("Mother's Education Level", min_value=0, max_value=4, value=2, step=1)
    Fedu = st.number_input("Father's Education Level", min_value=0, max_value=4, value=2, step=1)

st.divider()

# -----------------------
# Academic & Lifestyle
# -----------------------
st.subheader("📊 Academic & Lifestyle Factors")

col5, col6 = st.columns(2)

with col5:
    studytime = st.number_input("Weekly Study Time (1–4)", min_value=1, max_value=4, value=2, step=1)
    failures = st.number_input("Number of Past Failures", min_value=0, max_value=10, value=0, step=1)

with col6:
    absences = st.number_input("Number of Absences", min_value=0, max_value=300, value=4, step=1)
    internet = st.selectbox("Internet Access at Home", ["yes", "no"], index=0)

st.divider()

# -----------------------
# Build Payload
# -----------------------
payload = {
    "school": school,
    "sex": sex,
    "age": int(age),
    "address": address,
    "famsize": famsize,
    "Pstatus": Pstatus,
    "Medu": int(Medu),
    "Fedu": int(Fedu),
    "internet": internet,
    "studytime": int(studytime),
    "failures": int(failures),
    "absences": int(absences),
    "subject": subject,
}

st.subheader("📦 Payload Being Sent to API")
st.code(json.dumps(payload, indent=2), language="json")

# -----------------------
# Prediction Button
# -----------------------
if st.button("🔍 Predict Student Risk", type="primary"):
    st.write("📤 Sending the following data to the prediction API:")
    st.json(payload)

    try:
        resp = requests.post(API_URL, json=payload, timeout=15)
        st.write("📡 API Response Status:", resp.status_code)

        if resp.status_code == 200:
            st.success("✅ Prediction Successful")
            st.json(resp.json())
        else:
            st.error("❌ API Error Occurred")
            try:
                st.json(resp.json())
            except Exception:
                st.code(resp.text)

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Could not reach API: {e}")
