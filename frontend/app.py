
import io
import os

import pandas as pd
import requests
import streamlit as st

# The backend is reached over the Docker network: "backend" is the name of the Flask container.
# BACKEND_URL can be overridden with an environment variable for local testing.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:7860")

st.set_page_config(page_title="SuperKart Sales Forecast", layout="centered")
st.title("SuperKart Sales Forecast")
st.write("Estimate the sales revenue of a product in a store. Use the form for one product, or upload a CSV file for many.")

# ---------------- Online (single) prediction ----------------
st.header("Single prediction")
with st.form("single_prediction"):
    col1, col2 = st.columns(2)
    with col1:
        product_weight = st.number_input("Product weight", min_value=1.0, max_value=30.0, value=12.66, step=0.01)
        product_sugar = st.selectbox("Sugar content", ["Low Sugar", "Regular", "No Sugar"])
        product_area = st.number_input("Allocated display area (ratio)", min_value=0.0, max_value=0.5, value=0.027, step=0.001, format="%.3f")
        product_mrp = st.number_input("Product MRP", min_value=1.0, max_value=500.0, value=117.08, step=0.01)
        product_id_char = st.selectbox("Product ID prefix", ["FD", "DR", "NC"], help="FD = food, DR = drinks, NC = non-consumable")
    with col2:
        product_category = st.selectbox("Product type category", ["Perishables", "Non Perishables"], index=1)
        store_size = st.selectbox("Store size", ["Small", "Medium", "High"], index=1)
        store_city = st.selectbox("City type", ["Tier 1", "Tier 2", "Tier 3"], index=1)
        store_type = st.selectbox("Store type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"], index=3)
        store_age = st.number_input("Store age (years)", min_value=0, max_value=100, value=16, step=1)
    submitted = st.form_submit_button("Predict sales")

if submitted:
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": product_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_city,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": int(store_age),
        "Product_Type_Category": product_category,
    }
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
        response.raise_for_status()
        st.success(f"Predicted sales: {response.json()['Sales']:,.2f}")
    except requests.exceptions.RequestException as error:
        st.error(f"Could not reach the prediction service: {error}")

# ---------------- Batch prediction ----------------
st.header("Batch prediction")
st.write("Upload a CSV file with the same ten columns as the form above.")
uploaded_file = st.file_uploader("CSV file", type=["csv"])

if uploaded_file is not None and st.button("Predict batch"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": ("batch.csv", uploaded_file.getvalue(), "text/csv")},
            timeout=120,
        )
        response.raise_for_status()
        predictions = response.json()
        result = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))
        result.insert(0, "Predicted_Sales", [predictions[str(i)] for i in range(len(result))])  # first column, so it is visible without scrolling
        st.success(f"Predicted sales for {len(result)} rows.")
        st.dataframe(result)
        st.download_button("Download predictions", result.to_csv(index=False), "superkart_predictions.csv", "text/csv")
    except requests.exceptions.RequestException as error:
        st.error(f"Could not reach the prediction service: {error}")
