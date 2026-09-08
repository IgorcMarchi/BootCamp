import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator

import numpy as np
import pandas as pd
from random import randint, sample
import datetime
import time
import calendar

args = { 
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
} 

def generate_random_dates(start, end, n):  #gera n datas entre inicio e fim
    dates = pd.Series(np.zeros(n)) #cria um series panda com "n" 0
    for i in range(n): #pra cada n
        dates[i] = start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds()))) #faz uma data aleatorio
    return(dates) 

def push_xcom_with_return(): 
    n = 1000000 #define n

    df = pd.DataFrame({'user_id': sample(range(90000000, 99999999), n),  #gera ids nesse campo
                    'order_id': np.random.choice(range(1000000, 2000000), n, replace = False), #id de pedidos
                    'order_date': generate_random_dates(datetime.date(2015, 1, 1),  #usa a funcao pra criar data
                                                        datetime.date(2017, 12, 31), 
                                                        n),
                    'number_of_products': np.random.choice(range(20), n, replace = True), #gera qntds de produtos
                    'total_amount': np.round(np.random.uniform(1, 5000, n), 2)}) #gera valores

    df = df.assign(day_of_week = df.order_date.apply(lambda x: calendar.day_name[x.weekday()])) #cria uma coluna nova pegando a data gerada e vendo o nome do dia da semana do dia
    
    df.user_id = df.user_id.astype('str')  
    df.order_id = df.order_id.astype('str') #converte pra string 

    return df  #retorna o dataframe

def get_pushed_xcom_with_return(**context):  #pega os dados do XCom
    print(context['ti'].xcom_pull(task_ids = 't0')) 

with DAG(dag_id = 'xcom_dag_big_aula', default_args = args, schedule_interval = "@once") as dag:  #dag em si
    t0 = PythonOperator( 
        task_id = 't0', 
        python_callable = push_xcom_with_return #funcao q vai ser chamada
    )

    t1 = PythonOperator( #tarefa de python
        task_id = 't1', 
        provide_context = True, 
        python_callable = get_pushed_xcom_with_return #funcao q vai ser chamada
    )

    t0 >> t1  #ordem de execucao