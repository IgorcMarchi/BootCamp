from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator 
from airflow.operators.bash_operator import BashOperator 

from datetime import datetime # importa funções para trabalhar com datas

default_args = { # define as configurações padrão
    'start_data' : datetime(2019, 1, 1), # informa a data inicial
    'owenr' : 'Airflow', # responsável pela DAG
    'email': 'owner@test.com' # email usado para notificações
    }

with DAG(dag_id = 'pool_dag_aula', schedule_interval = '0 0 * * *', default_args = default_args, catchup = False) as dag: # cria e configura a DAG
    get_forex_rate_EUR = SimpleHttpOperator( # realiza a consulta da cotação do euro
        task_id = 'get_forex_rate_EUR', # nome de identificação da tarefa
        method = 'GET', # utiliza uma requisição do tipo GET
        priority_weight = 1, # estabelece o nível de prioridade
        pool = 'forex_api_pool', # associa a tarefa ao pool
        http_conn_id = 'forex_api', # utiliza a conexão cadastrada no Airflow
        endpoint = '/latest?base=EUR', # caminho utilizado para consultar a API
        xcom_push = True # salva o resultado no XCom
    )
    
    get_forex_rate_USD = SimpleHttpOperator( # consulta os dados referentes ao dólar
        task_id = 'get_forex_rate_USD', # identificação da tarefa
        method = 'GET', # faz uma requisição GET
        priority_weight = 2, # determina a prioridade da execução
        pool = 'forex_api_pool', # utiliza o mesmo pool de requisições
        http_conn_id = 'forex_api', # seleciona a conexão com a API
        endpoint = '/latest?base=USD', # consulta os valores com base no dólar
        xcom_push = True # envia o resultado para o XCom
    )
    
    get_forex_rate_JPY = SimpleHttpOperator( # busca os dados relacionados ao iene
        task_id = 'get_forex_rate_JPY', # identifica esta tarefa
        method = 'GET', # define o método da requisição
        priority_weight = 3, # configura a prioridade da tarefa
        pool = 'forex_api_pool', # adiciona a execução ao pool definido
        http_conn_id = 'forex_api', # usa a conexão configurada anteriormente
        endpoint = '/latest?base=JPY', # consulta a API utilizando o iene como base
        xcom_push = True # disponibiliza a resposta através do XCom
    )
    
    bash_command="""{% for task in dag.task_ids %} echo "{{ task }}" echo "{{ ti.xcom_pull(task) }}" {% endfor %}""" # percorre as tarefas e exibe seus resultados
    
    show_data = BashOperator(task_id = 'show_result', bash_command = bash_command) # apresenta os dados obtidos
    
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data # define que as consultas devem terminar antes de mostrar os resultados