import os
import random
import pandas as pd
import numpy as np
from __init__ import GENERATED_FILES_TARGET_LOCATION,CORRUPTION_METHODS

def split_df_in_batches(df: pd.DataFrame, batch_size: int):
    """Splits a large DataFrame into smaller DataFrames of specified number of rows."""
    number_dfs = len(df) // batch_size
    dataframes = []
    for i in range(number_dfs):
        start_index = i * batch_size
        end_index = (i + 1) * batch_size
        small_df = df.iloc[start_index:end_index].reset_index(drop=True)
        dataframes.append(small_df)
    if len(df) % batch_size != 0:
        dataframes.append(df.iloc[number_dfs * batch_size:].reset_index(drop=True))
    return dataframes

def generate_dataframes(csv_path, num_files, target_location=GENERATED_FILES_TARGET_LOCATION, columns_to_corrupt=None):
    
    df = pd.read_csv(csv_path)
    total_rows = len(df)
    rows_per_df = (total_rows + num_files - 1) // num_files

    if columns_to_corrupt is None:
        columns_to_corrupt = df.columns.tolist()

    dataframes = split_df_in_batches(df, rows_per_df)
    corruption_interval = random.randint(3, 10)
    corrupted_files = []
    os.makedirs(target_location, exist_ok=True)

    for df_index, dataframe in enumerate(dataframes):
        if (df_index + 1) % corruption_interval == 0:
            corrupted_dataframe = corrupt_dataframe(dataframe, rows_per_df, columns_to_corrupt)
            csv_filename = f'corrupted_dataframe_{df_index + 1}.csv'
            corrupted_files.append(csv_filename)  # Track corrupted files
            csv_file_path = os.path.join(target_location, csv_filename)
            corrupted_dataframe.to_csv(csv_file_path, index=False)
        else:
            csv_filename = f'dataframe_{df_index + 1}.csv'
            csv_file_path = os.path.join(target_location, csv_filename)
            dataframe.to_csv(csv_file_path, index=False)
    result_dict = {
        "Number of files created": len(dataframes),
        "Corruption Interval": corruption_interval,
    }
    return result_dict


def save_dataframes(dataframes, target_location):
    os.makedirs(target_location, exist_ok=True)
    for df_index, dataframe in enumerate(dataframes):
        csv_filename = f'dataframe_{df_index + 1}.csv'
        csv_file_path = os.path.join(target_location, csv_filename)
        dataframe.to_csv(csv_file_path, index=False)
    
    return len(dataframes)

import random
import pandas as pd

def corrupt_dataframe(dataframe, rows_per_df, columns_to_corrupt):
    corruption_methods = {
        'insert_na': lambda x, col: pd.NA,
        'random_string': lambda x, col: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
        'negative_value': lambda x, col: -abs(x) if col != 'Temperature' else x,
        'change_type': lambda x, col: str(x),
        'comma_for_decimal': lambda x, col: f"{x:.2f}".replace('.', ','),
        'extreme_value': lambda x, col: x * random.choice([1000000, -1000000])
    }
    
    corrupted_df = dataframe.copy()
    num_rows_to_corrupt = random.randint(1, min(rows_per_df, len(corrupted_df)))

    for row in random.sample(range(len(corrupted_df)), k=num_rows_to_corrupt):
        for col in random.sample(columns_to_corrupt, k=random.randint(1, len(columns_to_corrupt))):
            current_value = corrupted_df.at[row, col]
            corruption_type = random.choice(list(corruption_methods.keys()))
            original_dtype = corrupted_df[col].dtype 

            if corrupted_df[col].dtype != 'object' and corruption_type in ['random_string', 'change_type', 'comma_for_decimal']:
                corrupted_df[col] = corrupted_df[col].astype('object')

            corrupted_value = corruption_methods[corruption_type](current_value, col)
            corrupted_df.at[row, col] = corrupted_value
            if corruption_type not in ['random_string', 'change_type', 'comma_for_decimal']:
                try:
                    corrupted_df[col] = corrupted_df[col].astype(original_dtype)
                except ValueError:
                    print(f"Cannot convert back column {col} to {original_dtype}")

    return corrupted_df

