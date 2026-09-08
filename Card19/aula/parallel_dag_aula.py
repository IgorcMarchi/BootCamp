from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

def process(p1): # função que recebe um valor e finaliza retornando done
    print(p1)
    return 'done'

with DAG(dag_id='parallel_dag_aula', schedule_interval='0 0 * * *', default_args=default_args, catchup=True) as dag:
    
    # Tasks dynamically generated 
    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 5'.format(t)) for t in range(1, 4)] # cria três tarefas que executam em paralelo

    task_4 = PythonOperator(task_id='task_4', python_callable=process, op_args=['my super parameter'])  # executa a função process através do Python
    
    task_5 = BashOperator(task_id='task_5', bash_command='echo "pipeline done"')

    tasks >> task_4 >> task_5 # organiza a sequência em que as tarefas serão executadas
        