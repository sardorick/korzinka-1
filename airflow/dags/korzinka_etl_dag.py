from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator 

from transform import transform_data  

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2), 
    'retries': 1 
}

dag = DAG(
    'korzinka_click_processing',
    default_args=default_args,
    schedule_interval="@daily" 
)

transform_task = PythonOperator(
    task_id='transform_click_data',
    python_callable=transform_data,
    dag=dag
)

# Task to create tables (Optional, run this once initially)
create_tables_task = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='analytics_db', # Use your connection ID
    sql='sql/create_tables.sql',
    dag=dag
)

# Task to load CSV data using COPY command
load_data_task = PostgresOperator(
    task_id='load_clicks_data',
    postgres_conn_id='analytics_db',  # Use your connection ID
    autocommit=True,
    sql="COPY clicks (click_id, publisher_id, click_timestamp, click_date, click_time, country_iso_code, city, os_name, os_version, browser, browser_version, device_type, publisher_category) FROM '/path/to/your/clicks_transformed.csv' DELIMITER ',' CSV HEADER;",
    dag=dag
)

# Set task dependencies 
transform_task >> create_tables_task >> load_data_task
