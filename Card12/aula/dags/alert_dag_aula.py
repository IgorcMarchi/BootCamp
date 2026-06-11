from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

def on_success_task(dict):
    print("on_success_task")
    print(dict)

def on_failure_task(dict):
    print("on_failure_task")
    print(dict)

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'retries': 3, # número de tentativas em caso de falha
    'retry_delay': timedelta(seconds=60), # tempo de espera entre as tentativas
    'emails': ['owner@test.com'], # lista de e-mails para notificação em caso de falha
    'email_on_failure': True, # habilita notificação por e-mail em caso de falha
    'email_on_retry': False, # desabilita notificação por e-mail em caso de falha
    'on_failure_callback': on_failure_task, # função de callback para falha da tarefa
    'on_success_callback': on_success_task, # função de callback para sucesso da tarefa
    'execution_timeout': timedelta(seconds=60) # tempo máximo de execução da tarefa
}

def on_success_dag(dict):
    print("on_success_dag")
    print(dict)

def on_failure_dag(dict):
    print("on_failure_dag")
    print(dict)


# definição da DAG com o ID 'alert_dag', agendamento diário às 0h, argumentos padrão, catchup habilitado 
# e timeout de execução de segundos
# além disso, são definidas funções de callback para sucesso e falha da DAG
with DAG(dag_id='alert_dag', schedule_interval="0 0 * * *", default_args=default_args, catchup=True, dagrun_timeout=timedelta(seconds=75), 
        on_success_callback=on_success_dag, on_failure_callback=on_failure_dag) as dag:
    
    # Task 1
    t1 = BashOperator(task_id='t1', bash_command="exit 1")
    
    # Task 2
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'")

    t1 >> t2