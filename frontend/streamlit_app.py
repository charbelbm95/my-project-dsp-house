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
    df = pd.read_csv(uploaded_file)
    try:
        response = requests.post("http://backend:8000/predict_csv/", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.write("Predictions:")
            st.dataframe(pd.DataFrame(predictions))
        else:
            st.write(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.write(f"Error: {e}")

# Fetch past predictions
st.header("Past Predictions")
source = st.selectbox("Select Source", options=["all", "webapp", "scheduled"])
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

if st.button("Fetch Predictions"):
    params = {
        "source": source,
        "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
        "end_date": end_date.strftime("%Y-%m-%d") if end_date else None
    }
    try:
        response = requests.get("http://backend:8000/predictions/", params=params)
        if response.status_code == 200:
            past_predictions = response.json().get("predictions")
            st.write("Filtered Predictions:")
            df = pd.DataFrame(past_predictions, columns=["Time", "Date", "Source", "Inputs", "Prediction"])
            st.dataframe(df)
        else:
            st.write(f"Error: {response.json().get('detail')}")
    except Exception as e:
        st.write(f"Error: {e}")
