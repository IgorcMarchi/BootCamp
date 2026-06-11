# project_b_aula.py é a copia do backfill_aula.py, mas com o nome da DAG e do arquivo alterados.

from airflow import DAG
#from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

# args padrão para a DAG
default_args = { 
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

# DAG para project b
with DAG(dag_id='project_b_aula', schedule_interval="0 0 * * *", default_args=default_args, catchup=False) as dag:
    
    # Tarefa 1
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Tarega 2
    bash_task_2 = BashOperator(task_id='bash_task_2', bash_command="echo 'second task'")

    bash_task_1 >> bash_task_2