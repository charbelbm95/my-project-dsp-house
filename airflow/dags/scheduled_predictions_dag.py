from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import os

dag = DAG(
    'send_csv_to_api',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Read CSV and send to API every 5 minutes',
    schedule_interval='*/5 * * * *',
    start_date=days_ago(1),
    catchup=False
)

def read_and_send_csv():
    folder_path = '../../good-data'
    api_url = 'http://backend:8000/predict_csv/'

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_path = os.path.join(folder_path, file_name)
            with open(csv_path, 'rb') as f:
                files = {'file': (file_name, f)}
                response = requests.post(api_url, files=files)
                print(f'Status Code: {response.status_code}, Response: {response.text}')

# Define the task
send_task = PythonOperator(
    task_id='scheduled_predictions',
    python_callable=read_and_send_csv,
    dag=dag,
)