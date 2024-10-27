from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from joblib import load
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI()

# Load the trained model and scaler
model = load("trained_linear_regression_model.joblib")
scaler = load("scaler.joblib")

# Define input data model
class PredictionInput(BaseModel):
    Temperature: float
    Exhaust_Vacuum: float
    Ambient_Pressure: float
    Relative_Humidity: float

# Database connection
conn = sqlite3.connect("predictions.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS predictions 
                  (id INTEGER PRIMARY KEY, 
                   inputs TEXT, 
                   prediction REAL,
                   prediction_time TIMESTAMP,
                   source TEXT)""")
conn.commit()

@app.post("/predict/")
async def predict(input_data: PredictionInput):
    data = [[input_data.Temperature, input_data.Exhaust_Vacuum, input_data.Ambient_Pressure, input_data.Relative_Humidity]]
    scaled_data = scaler.transform(data)
    prediction = model.predict(scaled_data)[0]

    # Save prediction to database with timestamp
    prediction_time = datetime.now()
    cursor.execute("INSERT INTO predictions (inputs, prediction, prediction_time, source) VALUES (?, ?, ?, ?)", 
                   (str(data), prediction, prediction_time, "webapp"))
    conn.commit()
    
    return {"prediction": prediction}

@app.post("/predict_csv/")
async def predict_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        scaled_data = scaler.transform(df)
        predictions = model.predict(scaled_data)
        df['Net_Hourly_Electrical_Energy_Output'] = predictions

        # Save predictions to database with timestamp and source as "scheduled"
        prediction_time = datetime.now()
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO predictions (inputs, prediction, prediction_time, source) VALUES (?, ?, ?, ?)", 
                           (str(row[:-1].tolist()), row['Net_Hourly_Electrical_Energy_Output'], prediction_time, "scheduled"))
        conn.commit()

        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predictions/")
async def get_past_predictions(start_date: str, end_date: str, source: str = "all", page: int = 1, page_size: int = 20):
    query = "SELECT * FROM predictions WHERE prediction_time BETWEEN ? AND ?"
    params = [start_date, end_date]

    if source != "all":
        query += " AND source = ?"
        params.append(source)
    
    query += " ORDER BY prediction_time DESC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    return {"predictions": rows}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
