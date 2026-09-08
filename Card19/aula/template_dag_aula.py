import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta 

sys.path.insert(1, '/usr/local/airflow/dags/scripts') # adiciona a pasta dos scripts ao caminho do sistema

from Aula.process_logs_aula import process_logs_func # carrega a função responsável pelos logs

TEMPLATED_LOG_DIR = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/""" # cria o caminho dos logs usando a data formatada

default_args = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1
        } # configura os parâmetros que serão usados por padrão

with DAG(dag_id = "template_dag_aula", schedule_interval = "@daily", default_args=default_args) as dag: # define a DAG para rodar diariamente
    t0 = BashOperator( # primeira tarefa executada pelo terminal
        task_id = "t0", 
        bash_command = "echo {{ ts_nodash }} - {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}" # exibe a data formatada no terminal
        )

    t1 = BashOperator( # tarefa responsável por gerar novos logs
        task_id = "generate_new_logs",
        bash_command = "./scripts/generate_new_logs.sh", 
        params = {'filename': 'log.csv'} 
        )

    t2 = BashOperator( # tarefa que realiza a verificação do arquivo
        task_id = "logs_exist", 
        bash_command = "test -f " + TEMPLATED_LOG_DIR + "log.csv", 
        )

    t3 = PythonOperator( # tarefa executada através de uma função Python
        task_id = "process_logs", 
        python_callable = process_logs_func, 
        provide_context = True, 
        templates_dict = {'log_dir': TEMPLATED_LOG_DIR}, 
        params = {'filename': 'log.csv'} 
        )

    
    t0 >> t1 >> t2 >> t3 # estabelece a sequência das tarefas