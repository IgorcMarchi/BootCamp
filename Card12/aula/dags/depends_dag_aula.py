from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

def second_task():
    #print('Hello from second_task')
    raise ValueError('This will turns the python task in failed state') # a execução desta tarefa resultará em um estado de falha

def third_task():
    print('Hello from third_task')
    #raise ValueError('This will turns the python task in failed state') # a execução desta tarefa resultará em um estado de falha

# definição da DAG com o ID 'depends_task', agendamento diário às 0h, argumentos padrão e timezone local
with DAG(dag_id='depends_task', schedule_interval="0 0 * * *", default_args=default_args) as dag:
    
    # Task 1
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'", wait_for_downstream=True) # faz com que a tarefa aguarde a conclusão de todas as tarefas dependentes antes de ser considerada concluída, mesmo que a tarefa em si tenha sido concluída com sucesso.
    
    # Task 2
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task) 
    # depend_on_past=True faz com que a tarefa só seja executada se a execução anterior da mesma tarefa tiver sido bem-sucedida. 
    # Se a execução anterior falhar, a tarefa atual não será executada, mesmo que as dependências anteriores tenham sido concluídas com sucesso.
    # Task 3
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    bash_task_1 >> python_task_2 >> python_task_3