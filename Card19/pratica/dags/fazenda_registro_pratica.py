import pendulum

from airflow.models import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
# imports

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.now().subtract(days=1),
} # argumentos padrao


def registrar(): # registra a ocorrencia

    print("Ocorrencia registrada no sistema da fazenda")


with DAG(
    dag_id='fazenda_registro_pratica',
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag: # DAG de registro

    registrar_ocorrencia = PythonOperator( # registra o resultado
        task_id='registrar_ocorrencia',
        python_callable=registrar
    )

    finalizar = EmptyOperator( # finaliza o fluxo
        task_id='finalizar'
    )

    # ordem das tasks
    registrar_ocorrencia >> finalizar