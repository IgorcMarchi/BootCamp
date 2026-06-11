import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator

from datetime import timedelta, datetime

local_tz = pendulum.timezone("Europe/Paris") # timezone local para a DAG

# definição dos argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 3, 29, 2, tzinfo=local_tz), # data de início da DAG com timezone local
    'owner': 'Airflow'
}

# definição da DAG com o ID 'tz_dag', agendamento diário às 1h da manhã, 
# argumentos padrão e timezone local
with DAG(dag_id='tz_dag', schedule_interval="0 2 * * *", default_args=default_args) as dag:
    dummy_task = DummyOperator(task_id='dummy_task') # tarefa dummy para a DAG
    
    run_dates = dag.get_run_dates(start_date=dag.start_date) # obtém as datas de execução da DAG a partir da data de início
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None # obtém a próxima data de execução da DAG, se houver execuções anteriores, caso contrário, None
    
    # Uncomment when you use the DAG, comment when not
    # print para verificar se a datetime do Python é ingênua (naive) e se a datetime do Airflow é consciente (aware), além de imprimir informações sobre a timezone, data de início, intervalo de agendamento, última data de execução e próxima data de execução em UTC e horário local
    print('datetime from Python is Naive: {0}'.format(timezone.is_naive(datetime(2019, 9, 19))))
    print('datetime from Airflow is Aware: {0}'.format(timezone.is_naive(timezone.datetime(2019, 9, 19)) == False))
    # print para verificar informações sobre a DAG, incluindo timezone, data de início, intervalo de agendamento, última data de execução e próxima data de execução em UTC e horário local
    print('[DAG:tz_dag] timezone: {0} - start_date: {1} - schedule_interval: {2} - Last execution_date: {3} - next execution_date {4} in UTC - next execution_date {5} in local time'.format(
        dag.timezone,  # timezone da DAG
        dag.default_args['start_date'],  # data de início da DAG
        dag._schedule_interval, # intervalo de agendamento da DAG
        dag.latest_execution_date, # última data de execução da DAG
        next_execution_date, # próxima data de execução da DAG em UTC
        local_tz.convert(next_execution_date) if next_execution_date is not None else None # próxima data de execução da DAG convertida para o horário local, se houver uma próxima data de execução
        ))