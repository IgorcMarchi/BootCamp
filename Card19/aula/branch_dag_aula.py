import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator # importa os operadores necessários

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
} # configura os valores padrão da DAG

IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json' # lista das APIs que serão verificadas
}

def check_api(): # verifica qual das APIs retorna uma resposta válida
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json()
            if data and 'country' in data and len(data['country']):
                return api
        except ValueError:
            pass
    return 'none'

with DAG(dag_id = 'branch_dag_aula', default_args = default_args, schedule_interval = "@once") as dag: # cria a DAG e define sua execução
    check_api = BranchPythonOperator( # escolhe qual caminho será seguido de acordo com a API disponível
        task_id = 'check_api',
        python_callable = check_api
    )

    none = DummyOperator( # utilizada caso nenhuma API seja encontrada
        task_id = 'none'
    )

    save = DummyOperator(task_id = 'save') # representa a etapa final do processo

    check_api >> none >> save # define o caminho quando nenhuma API funciona

    for api in IP_GEOLOCATION_APIS: # cria uma tarefa para cada API da lista
        process = DummyOperator(
            task_id = api
        )
    
        check_api >> process >> save # conecta cada possibilidade com a etapa final