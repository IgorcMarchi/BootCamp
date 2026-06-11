from airflow import DAG
from datetime import datetime, timedelta
from airflow.sensor.http_sensor import HttpSensor
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.slack_operator import SlackAPIPostOperator
import json
import csv
import requests


default_args = {
    "owner": "airflow", # proprietário da DAG
    "start_date": datetime(2025, 5, 23), # data de início da DAG
    "depends_on_past": False, # não depende de execuções anteriores
    "email_on_failure": False, # notificação para email em caso de falha
    "email_on_retry": False, # notificação para email em caso de reiniciar
    "email": ["youremail@host.com"], # email para notificações
    "retries": 1, # número de tentativas em caso de falha
    "retry_delay": timedelta(minutes=5), # tempo de espera entre as tentativas
}

# função para baixar as taxas de câmbio
def download_rates():
    with open('/usr/local/airflow/dags/files/forex_currencies.csv') as forex_currencies:
        reader = csv.DictReader(forex_currencies, delimiter=';')
        for row in reader:
            base = row['base']
            with_pairs = row['with_pairs'].split(' ')
            indata = requests.get('https://api.exchangeratesapi.io/latest?base=' + base).json()
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}
            for pair in with_pairs:
                outdata['rates'][pair] = indata['rates'][pair]
            with open('/usr/local/airflow/dags/files/forex_rates.json', 'a') as outfile:
                json.dump(outdata, outfile)
                outfile.write('\n')

# definição da DAG
with DAG(dag_id="forex_data_pipeline", 
         schule_interval="@daily",  # agendamento diário
         default_args=default_args, # argumentos padrão para as tarefas
         catchup=False) as dag: # não executar tarefas anteriores ao start_date
    
    # tarefa para verificar a disponibilidade dos dados de Forex
    is_forex_rates_available = HttpSensor( 
        task_id="is_forex_rates_available", # ID da tarefa
        method='GET', # método HTTP para a requisição
        http_conn_id='forex_api', # conexão HTTP configurada no Airflow para a API de Forex
        endpoint='latest', # endpoint para verificar a disponibilidade dos dados
        response_check=lambda response: "rates" in response.text, # verifica se a resposta contém "rates"
        poke_interval=5, # intervalo de verificação em segundos
        timeout=20 # tempo máximo de espera em segundos
    )

    # tarefa para verificar a disponibilidade do arquivo de moedas de Forex
    is_forex_currencies_file_available = FileSensor(
        task_id="is_forex_currencies_file_available", # ID da tarefa
        fs_conn_id="forex_data", # conexão de arquivos configurada no Airflow para os dados de Forex
        filepath="forex_currencies.csv", # caminho do arquivo a ser verificado
        poke_interval=5, # intervalo de verificação em segundos
        timeout=20 # tempo máximo de espera em segundos
    )

    # tarefa para baixar as taxas de câmbio
    downloading_rates = PythonOperator(
        task_id="downloading_rates", # ID da tarefa
        python_callable=download_rates # função Python a ser executada para baixar as taxas de câmbio
    )

    # tarefa para salvar as taxas de câmbio no HDFS
    saving_rates = BashOperator(
        task_id="saving_rates", # ID da tarefa
        # comando bash para criar o diretório no HDFS e salvar o arquivo de taxas de câmbio
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
            """
    )

    # tarefa para criar a tabela de taxas de câmbio no Hive
    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table", # ID da tarefa
        hive_cli_conn_id="hive_conn", # conexão Hive configurada no Airflow
        # comando HQL para criar a tabela de taxas de câmbio no Hive
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    # tarefa para processar as taxas de câmbio usando Spark
    forex_processing = SparkSubmitOperator(
        task_id="forex_processing", # ID da tarefa
        conn_id="spark_conn", # conexão Spark configurada no Airflow
        application="/usr/local/airflow/dags/scripts/forex_processing.py", # caminho do script Spark para processar as taxas de câmbio
        verbose=False # não exibir logs detalhados do Spark
    )
    # tarefa para enviar uma notificação por email após o processamento das taxas de câmbio
    sending_email_notification = EmailOperator(
        task_id="sending_email_notification", # ID da tarefa
        to="airflow_course@yopmail.com", # destinatário do email
        subject="forex_data_pipeline", # assunto do email
        html_content="<h3>forex_data_pipeline succeeded</h3>" # conteúdo do email em HTML
    )

    # tarefa para enviar uma notificação por Slack após o processamento das taxas de câmbio
    sending_slack_notification = SlackAPIPostOperator(
        task_id="sending_slack", # ID da tarefa
        token="xoxp-11296979307255-11309057656005-11310408451718-146649eefbf53a7a5856611140e35ead", # token de autenticação do Slack
        username="airflow", # nome de usuário para a mensagem do Slack
        text="DAG forex_data_pipeline: DONE", # texto da mensagem do Slack
        channel="#airflow--exploit" # canal do Slack onde a mensagem será enviada
    )

    is_forex_rates_available >> is_forex_currencies_file_available >> downloading_rates >> saving_rates >> creating_forex_rates_table >> forex_processing >> sending_email_notification >> sending_slack_notification
