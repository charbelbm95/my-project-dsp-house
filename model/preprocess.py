import numpy as np
import pandas as pd
from typing import TextIO
from sklearn.preprocessing import StandardScaler
from pandas.api.types import is_numeric_dtype



def identify_null_rows(df: pd.DataFrame):
    """ reports which rows were dropped and in which columns were the null values. """
    null_data = df[df.isnull().any(axis=1)]
    if not null_data.empty:
        for index, row in null_data.iterrows():
            null_columns = row[row.isnull()].index.tolist()
            print(f"Row {index} dropped due to null values in columns: {', '.join(null_columns)}")


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Preprocess the given DataFrame by removing any rows with null or missing values,
    and ensuring all data is numerical. Raises an error if non-numerical data is found."""
    
    identify_null_rows(df)
    cleaned_df = df.dropna()
    non_numeric_values = []

    for column in cleaned_df.columns:
        if not is_numeric_dtype(cleaned_df[column]):
            for index, value in cleaned_df[column].items():
                try:
                    float(value)
                except ValueError:
                    non_numeric_values.append((column, index, value))
    if non_numeric_values:
        error_message = "\n".join([f"Non-numerical value found in column '{col}' at row {idx}: {val}" 
                                  for col, idx, val in non_numeric_values])
        raise ValueError(error_message)

    return cleaned_df


def standardize_data(df: pd.DataFrame) -> tuple[pd.DataFrame, StandardScaler]:
    """Standardize numerical features."""
    scaler = StandardScaler()
    scaler.fit(df)
    df = scaler.transform(df)
    return df, scaler

