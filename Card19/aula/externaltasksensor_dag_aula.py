import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta # importa recursos de data e tempo

default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    } # define as configurações padrão da DAG

with DAG(dag_id = "externaltasksensor_dag_aula", default_args = default_args, schedule_interval = "@daily") as dag: # cria a DAG com execução diária
    
    sensor = ExternalTaskSensor( # cria um sensor para acompanhar uma tarefa externa
        task_id = 'sensor', # define a identificação do sensor
        external_dag_id = 'sleep_dag', # informa qual DAG será monitorada
        external_task_id = 't2' # indica qual tarefa da DAG externa deve ser aguardada
    )

    last_task = DummyOperator(task_id = "last_task") # representa a etapa final do fluxo

    sensor >> last_task # executa a tarefa final somente depois que o sensor for concluído