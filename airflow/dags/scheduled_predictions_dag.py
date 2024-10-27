from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowSkipException
import pandas as pd
import requests
import os
import shutil

dag = DAG(
    'scheduled_predictions',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Read CSV and send to API every 60 seconds',
    schedule_interval=timedelta(seconds=60),
    start_date=days_ago(1),
    catchup=False
)

def read_and_send_csv():
    folder_path = '/opt/good-data/'  
    predicted_data_path = '/opt/predicted-data/'  
    api_url = 'http://backend:8000/predict_csv/'  

    os.makedirs(predicted_data_path, exist_ok=True)

    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        raise AirflowSkipException("No CSV files found in the good-data directory.")

    file_name = csv_files[0]
    csv_path = os.path.join(folder_path, file_name)
    with open(csv_path, 'rb') as f:
        files = {'file': (file_name, f)}
        response = requests.post(api_url, files=files)
        print(f'Status Code: {response.status_code}, Response: {response.text}')

    shutil.move(csv_path, os.path.join(predicted_data_path, file_name))

send_task = PythonOperator(
    task_id='scheduled_predictions',
    python_callable=read_and_send_csv,
    dag=dag,
)
