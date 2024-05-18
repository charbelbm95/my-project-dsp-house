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

# Fetch past predictions
st.header("Past Predictions")
start_date = st.date_input("Start date")
end_date = st.date_input("End date")
source = st.selectbox("Source", ["all", "webapp", "scheduled"])

if st.button("Fetch Predictions"):
    try:
        response = requests.get(
            f"http://backend:8000/predictions/",
            params={"start_date": start_date, "end_date": end_date, "source": source}
        )
        if response.status_code == 200:
            past_predictions = response.json().get("predictions")
            df = pd.DataFrame(past_predictions, columns=["ID", "Inputs", "Prediction", "Prediction Time", "Source"])
            st.write("Past Predictions:")
            st.table(df)
        else:
            st.write(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.write(f"Error: {e}")