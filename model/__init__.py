import os
RANDOM_STATE = 42
TRAINING_TEST_SIZE = 0.25
FEATURES_LIST = ['Temperature','Exhaust Vacuum','Ambient Pressure','Relative Humidity']
TARGET_VARIABLE = 'Net Hourly Electrical Energy Output'
GENERATED_FILES_TARGET_LOCATION =  '../raw-data'
GENERATED_FILES_SOURCE_LOCATON = '../data/data-generation-source-power-data.csv'
MODEL_LOCATION = '../backend/trained_linear_regression_model.joblib'
SCALER_LOCATION = '../backend/scaler.joblib'
TRAINING_DATA_PATH = '../data/power-data.csv'
TESTING_DATA_PATH = '../data/preprocessed-x-test-data.csv'
CORRUPTION_METHODS = {
        'insert_na': lambda x, col: pd.NA,
        'random_string': lambda x, col: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
        'negative_value': lambda x, col: -abs(x) if col != 'Temperature' else x,
        'change_type': lambda x, col: str(x),
        'comma_for_decimal': lambda x, col: f"{x:.2f}".replace('.', ','),
        'extreme_value': lambda x, col: x * random.choice([10000, -10000])
    }

