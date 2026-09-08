from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

def process(p1): # função responsável por receber e exibir o parâmetro
    print(p1)
    return 'done'

with DAG(dag_id='next_dag_aula', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tasks dynamically generated 
    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 5'.format(t)) for t in range(1, 4)]

    task_4 = PythonOperator(task_id='task_4', python_callable=process, op_args=['my super parameter']) # executa a função process

    task_5 = BashOperator(task_id='task_5', bash_command='echo "pipeline done"') # exibe uma mensagem ao finalizar o pipeline

    tasks >> task_4 >> task_5 # determina a sequência de execução das tarefas
        