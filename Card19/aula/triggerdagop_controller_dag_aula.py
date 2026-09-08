import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator 

default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    } 

def conditionally_trigger(context, dag_run_obj): # função responsável por decidir se outra DAG será acionada
    if context['params']['condition_param']: 
        dag_run_obj.payload = { # monta os dados que serão enviados para a próxima DAG
                'message': context['params']['message'] # adiciona a mensagem ao conteúdo enviado
            }
        pp.pprint(dag_run_obj.payload) # exibe os dados enviados
        return dag_run_obj 

with DAG(dag_id="triggerdagop_controller_dag_aula", default_args=default_args, schedule_interval="@once") as dag: # cria a DAG para executar uma vez
    
    trigger = TriggerDagRunOperator( # cria a tarefa responsável por iniciar outra DAG
        task_id = "trigger_dag", 
        trigger_dag_id = "triggerdagop_target_dag", 
        provide_context = True, 
        python_callable = conditionally_trigger, 
        params = { # valores enviados para a função
            'condition_param': True, 
            'message': 'Hi from the controller'
        },
    )

    last_task = DummyOperator(task_id = "last_task") # representa a etapa final do fluxo

    trigger >> last_task # executa a tarefa final depois do disparo da outra DAG