import airflow
from subdags.subdag import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.celery_executor import CeleryExecutor # importa os recursos necessários

DAG_NAME="deadlock_subdag_aula" # define o nome utilizado pela DAG

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
} 

with DAG(dag_id=DAG_NAME, default_args=default_args, schedule_interval="@once") as dag: # cria a DAG para uma única execução
    start = DummyOperator( # representa o ponto inicial do fluxo
        task_id='start'
    )

    subdag_1 = SubDagOperator( 
        task_id='subdag-1', 
        subdag=factory_subdag(DAG_NAME, 'subdag-1', default_args), # gera a primeira SubDAG
        executor=CeleryExecutor() # utiliza o Celery para executar as tarefas
    )
 
    subdag_2 = SubDagOperator( # configura a segunda SubDAG
        task_id='subdag-2',
        subdag=factory_subdag(DAG_NAME, 'subdag-2', default_args), # gera o fluxo interno da segunda SubDAG
        executor=CeleryExecutor() # define o Celery como executor
    )

    subdag_3 = SubDagOperator( # configura a terceira SubDAG
        task_id='subdag-3',
        subdag=factory_subdag(DAG_NAME, 'subdag-3', default_args), # cria o conteúdo da terceira SubDAG
        executor=CeleryExecutor() # executa através do Celery
    )

    subdag_4 = SubDagOperator( # configura a quarta SubDAG
        task_id='subdag-4',
        subdag=factory_subdag(DAG_NAME, 'subdag-4', default_args), # gera a última SubDAG do fluxo
        executor=CeleryExecutor()
    )

    final = DummyOperator( # representa o encerramento do fluxo
        task_id='final'
    )

    start >> [subdag_1, subdag_2, subdag_3, subdag_4] >> final 
    # executa as SubDAGs após o início e depois segue para a tarefa final