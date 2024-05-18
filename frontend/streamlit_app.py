import streamlit as st
import requests
import pandas as pd

st.title("ML Model Prediction App")

# User input for prediction
st.header("Single Prediction")
temperature = st.number_input("Temperature")
exhaust_vacuum = st.number_input("Exhaust Vacuum")
ambient_pressure = st.number_input("Ambient Pressure")
relative_humidity = st.number_input("Relative Humidity")

if st.button("Predict"):
    input_data = {
        "Temperature": temperature,
        "Exhaust_Vacuum": exhaust_vacuum,
        "Ambient_Pressure": ambient_pressure,
        "Relative_Humidity": relative_humidity
    }
    try:
        response = requests.post("http://backend:8000/predict/", json=input_data)
        if response.status_code == 200:
            prediction = response.json().get("prediction")
            st.write("Prediction:")
            df = pd.DataFrame([input_data])
            df["Prediction"] = prediction
            st.table(df)
        else:
            st.write(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.write(f"Error: {e}")

# CSV upload for batch prediction
st.header("Batch Prediction")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    try:
        response = requests.post("http://backend:8000/predict_csv/", files={"file": uploaded_file.getvalue()})
        if response.status_code == 200:
            predictions = response.json()
            df = pd.DataFrame(predictions)
            st.write("Batch Predictions:")
            st.table(df)
        else:
            st.write(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.write(f"Error: {e}")

# Function to fetch past predictions with pagination
def fetch_predictions(start_date, end_date, source, page, page_size):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "source": source,
        "page": page,
        "page_size": page_size
    }
    response = requests.get("http://backend:8000/predictions/", params=params)
    if response.status_code == 200:
        return response.json()["predictions"]
    else:
        st.error(f"Error fetching predictions: {response.status_code}")
        return []

# Fetch past predictions with pagination
st.header("Past Predictions")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
source = st.selectbox("Source", ["all", "webapp", "scheduled"])

page = st.number_input("Page", min_value=1, step=1, value=1)
page_size = 20

if st.button("Fetch Predictions"):
    predictions = fetch_predictions(start_date, end_date, source, page, page_size)
    if predictions:
        df = pd.DataFrame(predictions, columns=["ID", "Inputs", "Prediction", "Prediction Time", "Source"])
        st.write("Past Predictions:")
        st.table(df)
    else:
        st.write("No predictions found for the selected criteria.")

# Navigation buttons for pagination
if st.button("Previous Page") and page > 1:
    page -= 1
    st.experimental_rerun()

if st.button("Next Page") and len(predictions) == page_size:
    page += 1
    st.experimental_rerun()
