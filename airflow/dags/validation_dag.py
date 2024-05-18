from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowSkipException
import os
import shutil
import great_expectations as ge

# Define the DAG
dag = DAG(
    'validate_csv',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Validate CSV files and move to good-data or bad-data',
    schedule_interval='*/2 * * * *',
    start_date=days_ago(1),
    catchup=False
)

def validate_csv():
    context = ge.data_context.DataContext("gx")
    folder_path = '/opt/raw-data/'  # Path to the mounted raw-data directory

    # Get the list of CSV files
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        raise AirflowSkipException("No CSV files found in the raw-data directory.")

    # Process the first CSV file
    file_name = csv_files[0]
    csv_path = os.path.join(folder_path, file_name)

    # Set up checkpoint
    checkpoint_config = {
        "name": "csv_checkpoint",
        "config_version": 1.0,
        "class_name": "Checkpoint",
        "run_name_template": "%Y%m%d-%H%M%S-validation",
        "expectation_suite_name": "data_expectations",
        "batch_request": {
            "datasource_name": "raw_data_source",
            "data_connector_name": "default_inferred_data_connector_name",
            "data_asset_name": file_name
        },
        "action_list": [
            {
                "name": "store_validation_result",
                "action": {
                    "class_name": "StoreValidationResultAction"
                }
            },
            {
                "name": "store_evaluation_params",
                "action": {
                    "class_name": "StoreEvaluationParametersAction"
                }
            },
            {
                "name": "update_data_docs",
                "action": {
                    "class_name": "UpdateDataDocsAction"
                }
            }
        ]
    }
    context.add_checkpoint(**checkpoint_config)
    checkpoint_result = context.run_checkpoint(checkpoint_name="csv_checkpoint")

    validation_success = checkpoint_result["success"]
    if validation_success:
        destination_path = os.path.join("/opt/good-data/", file_name)
    else:
        destination_path = os.path.join("/opt/bad-data/", file_name)

    shutil.move(csv_path, destination_path)

# Define the task
validate_task = PythonOperator(
    task_id='validate_csv',
    python_callable=validate_csv,
    dag=dag,
)
