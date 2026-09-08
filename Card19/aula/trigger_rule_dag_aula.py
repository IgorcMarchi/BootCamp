import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
} 

def download_website_a():
    print("download_website_a")

def download_website_b():
    print("download_website_b")

def download_failed():
    print("download_failed")

def download_succeed():
    print("download_succeed")
#printa o status dos  downloads

def process():
    print("process")

def notif_a():
    print("notif_a")

def notif_b():
    print("notif_b")

with DAG(dag_id = 'trigger_rule_dag_aula', default_args = default_args, schedule_interval = "@daily") as dag: #DAG
    
    download_website_a_task = PythonOperator( # tarefa responsável pelo download do site A
        task_id = 'download_website_a', 
        python_callable = download_website_a, #funcao sendo chamado
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    download_website_b_task = PythonOperator( # tarefa responsável pelo download do site B
        task_id = 'download_website_b', 
        python_callable = download_website_b, #chamando a funcao 
        trigger_rule = "all_success"    #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    download_failed_task = PythonOperator( # tarefa utilizada para indicar erro no download
        task_id = 'download_failed', 
        python_callable = download_failed, #funcao q vai ser chamada
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    download_succeed_task = PythonOperator( # tarefa utilizada para indicar sucesso no download
        task_id = 'download_succeed', 
        python_callable = download_succeed, 
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    process_task = PythonOperator( # cria a tarefa de notificação process
        task_id = 'process', 
        python_callable = process, 
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    notif_a_task = PythonOperator( # cria a tarefa de notificação A
        task_id = 'notif_a', 
        python_callable = notif_a, 
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )

    notif_b_task = PythonOperator( # cria a tarefa de notificação B
        task_id = 'notif_b', 
        python_callable = notif_b, 
        trigger_rule = "all_success" #so vai ser executada quando todas as tasks anteriores tiverem sucesso
    )