import random
import pendulum

from airflow.models import DAG
from airflow.providers.standard.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
# imports

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.now().subtract(days=1),
} # argumentos padrao


def gerar_dados(): # gera dados dos sensores

    dados = {
        'temperatura': random.randint(20, 45),
        'agua': random.randint(10, 100),
        'racao': random.randint(10, 100)
    }

    print("Temperatura:", dados['temperatura'])
    print("Agua:", dados['agua'])
    print("Racao:", dados['racao'])

    return dados # manda os dados pro XCom


def verificar_sensores(**context): # verifica os sensores

    dados = context['ti'].xcom_pull(
        task_ids='coletar_dados'
    ) # pega os dados do XCom

    if dados['temperatura'] > 38:
        print("Temperatura muito alta")
        return 'acionar_emergencia'

    if dados['agua'] < 30:
        print("Nivel de agua baixo")
        return 'acionar_emergencia'

    if dados['racao'] < 25:
        print("Nivel de racao baixo")
        return 'acionar_emergencia'

    print("Tudo normal na fazenda")
    return 'fazenda_normal'


with DAG(
    dag_id='fazenda_monitoramento_pratica',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag: # DAG principal

    coletar = PythonOperator( # coleta os dados
        task_id='coletar_dados',
        python_callable=gerar_dados
    )

    verificar = BranchPythonOperator( # escolhe o caminho
        task_id='verificar_sensores',
        python_callable=verificar_sensores
    )

    normal = EmptyOperator( # caso esteja tudo normal
        task_id='fazenda_normal'
    )

    emergencia = TriggerDagRunOperator( # chama a DAG de emergencia
        task_id='acionar_emergencia',
        trigger_dag_id='fazenda_emergencia_pratica',
        conf={
            'motivo': 'problema_detectado'
        }
    )

    # ordem das tasks
    coletar >> verificar
    verificar >> [normal, emergencia]