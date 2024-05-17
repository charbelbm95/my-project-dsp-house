import numpy as np
import pandas as pd
import joblib
from typing import Union,TextIO
from sklearn.preprocessing import StandardScaler
from preprocess import preprocess_data
from __init__ import  FEATURES_LIST,TARGET_VARIABLE,SCALER_LOCATION,MODEL_LOCATION



def transform_data(df: pd.DataFrame,scaler: StandardScaler) -> pd.DataFrame:
    """Transform the data using the provided scaler and encoder."""
    output_df = df.copy()
    output_df = df.astype(float)
    output_df = scaler.transform(df)
    return output_df

def make_predictions(input_data: Union[TextIO, pd.DataFrame, dict]) -> np.ndarray:
    """Make predictions using the trained model based on the type of input data"""
    loaded_scaler = joblib.load(SCALER_LOCATION)
    loaded_model = joblib.load(MODEL_LOCATION)

    if isinstance(input_data, TextIO):
        with input_data as file:
            df = pd.read_csv(file)
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    elif isinstance(input_data, dict):
        df = pd.DataFrame.from_dict([input_data])
    else:
        raise ValueError("Unsupported input type. Please provide a CSV file, Pandas DataFrame, or dictionary.")

    X_testing = df[FEATURES_LIST]
    X_testing = preprocess_data(X_testing) 
    X_testing = transform_data(X_testing, loaded_scaler)  
    return loaded_model.predict(X_testing)
