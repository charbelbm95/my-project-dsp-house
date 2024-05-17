import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_log_error
from sklearn.preprocessing import StandardScaler
from preprocess import standardize_data
from __init__ import FEATURES_LIST, TARGET_VARIABLE, RANDOM_STATE,TRAINING_TEST_SIZE,MODEL_LOCATION,SCALER_LOCATION


def compute_rmsle(y_true: np.ndarray,
                  y_pred: np.ndarray,
                  precision: int = 2) -> float:
    """Compute the Root Mean Squared Logarithmic Error."""
    rmsle = np.sqrt(mean_squared_log_error(y_true, y_pred))
    return round(rmsle, precision)


def prepare_data(
    df: pd.DataFrame,
    scaler: StandardScaler = None,
    fit_transform: bool = True
) -> tuple[pd.DataFrame, StandardScaler]:
    """Prepare the data by standardizing """
    if fit_transform:
        df, scaler = standardize_data(df)
    else:
        df = scaler.transform(df)
    return df, scaler


def build_model(data: pd.DataFrame) -> dict[str, float]:
    """Build and evaluate the model from the provided DataFrame."""
    X_train, X_test, y_train, y_test = train_test_split(
        data[FEATURES_LIST],
        data[TARGET_VARIABLE],
        test_size=TRAINING_TEST_SIZE,
        random_state=RANDOM_STATE)
    X_train, scaler= prepare_data(X_train, fit_transform=True)
    joblib.dump(scaler, SCALER_LOCATION)
    X_test, _ = prepare_data(X_test,  scaler, fit_transform= False)
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_LOCATION)
    y_pred = model.predict(X_test)
    return {'r2-score': round(r2_score(y_test, y_pred),2), 'rmsle': compute_rmsle(y_test, y_pred)}
