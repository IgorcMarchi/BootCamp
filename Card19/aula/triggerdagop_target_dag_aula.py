import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator #imports

default_args = {
    "start_date": airflow.utils.dates.days_ago(1), 
    "owner": "Airflow"
} 

def remote_value(**context): #funcao q pega valores recebidos da dag
    print("Value {} for key=message received from the controller DAG".format(context["dag_run"].conf["message"])) #imprime os dados q chegaram

with DAG(dag_id = "triggerdagop_target_dag_aula", default_args = default_args, schedule_interval = None) as dag: #dag em si

    t1 = PythonOperator( #operador python
            task_id = "t1", 
            provide_context = True, #deixa passar contexto pra outras dags
            python_callable = remote_value,  #funcao q vai ser chamada
        )

    t2 = BashOperator( #tarefa de terminal
        task_id = "t2", 
        bash_command = 'echo Message: {{ dag_run.conf["message"] if dag_run else "" }}') #comando q vai rodar no terminal 

    t3 = BashOperator(  #tarefa de terminal
        task_id = "t3",
        bash_command = "sleep 30" #comando do terminal
    )