from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from crawl_data import main as crawler
from move_data_to_blob_storage import main as move_data


def print_hello():
    print('Hello!')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 25),
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'hello_world',
    default_args=default_args,
    description='crawl data dag',
    schedule_interval=timedelta(days=1),
)


crawler_operator = PythonOperator(task_id='crawler_task',
                                  python_callable=crawler, dag=dag)

move_data_to_blob_storage_operator = PythonOperator(task_id='move_data_task',
                                                    python_callable=move_data, dag=dag)

crawler_operator >> move_data_to_blob_storage_operator
