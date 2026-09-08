from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operator.bash_operator import BashOperator

from datetime import datetime 

default_args = {
    'start_data' : datetime(2019, 1, 1),
    'owenr' : 'Airflow', 
    'email': 'owner@test.com' 
}

with DAG(dag_id = 'queue_dag_aula', schedule_interval = '0 0 * * *', default_args = default_args, catchup = False) as dag:
    t_1_ssd = BashOperator(task_id = 't_1_ssd', bash_command = 'echo "I/O intensive task"', queue = 'worker_ssd') # executa uma tarefa de I/O utilizando a fila do SSD
    
    t_2_ssd = BashOperator(task_id = 't_2_ssd', bash_command = 'echo "I/O intensive task"', queue = 'worker_ssd') # envia outra tarefa de I/O para o worker SSD
    
    t_3_ssd = BashOperator(task_id = 't_3_ssd', bash_command = 'echo "I/O intensive task"', queue = 'worker_ssd') # executa o processo através da fila worker_ssd
    
    t_4_cpu = BashOperator(task_id = 't_4_cpu', bash_command = 'echo "CPU intensive task"', queue = 'worker_cpu') # direciona uma tarefa de processamento para o worker CPU
    
    t_5_cpu = BashOperator(task_id = 't_5_cpu', bash_command = 'echo "CPU intensive task"', queue = 'worker_cpu') # executa outra tarefa utilizando a fila da CPU
    
    t_6_spark = BashOperator(task_id = 't_6_spark', bash_command = 'echo "Spark dependecy task"', queue = 'worker_spark') # direciona a tarefa relacionada ao Spark para seu worker
    
    task_7 = DummyOperator(task_id = 'task_7') # cria uma tarefa sem processamento
    
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7 # a tarefa 7 só inicia depois que todas as anteriores terminarem