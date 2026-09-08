import pendulum

from airflow.models import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
# imports

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.now().subtract(days=1),
} # argumentos padrao


def receber_alerta(**context): # recebe o alerta

    motivo = context['dag_run'].conf.get(
        'motivo',
        'nao informado'
    )

    print("Emergencia recebida:", motivo)


def finalizar_atendimento(): # finaliza a verificacao

    print("Verificacao da fazenda concluida")


with DAG(
    dag_id='fazenda_emergencia_pratica',
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag: # DAG de emergencia

    alerta = PythonOperator( # recebe o alerta
        task_id='receber_alerta',
        python_callable=receber_alerta
    )

    with TaskGroup(
        group_id='verificar_setores'
    ) as setores: # agrupa as verificacoes

        verificar_agua = EmptyOperator(
            task_id='verificar_agua'
        )

        verificar_racao = EmptyOperator(
            task_id='verificar_racao'
        )

        verificar_temperatura = EmptyOperator(
            task_id='verificar_temperatura'
        )

        verificar_animais = EmptyOperator(
            task_id='verificar_animais'
        )

    concluir = PythonOperator( # encerra o atendimento
        task_id='atendimento_concluido',
        python_callable=finalizar_atendimento
    )

    registrar = TriggerDagRunOperator( # chama a DAG de registro
        task_id='chamar_registro',
        trigger_dag_id='fazenda_registro_pratica'
    )

    # ordem das tasks
    alerta >> setores >> concluir >> registrar