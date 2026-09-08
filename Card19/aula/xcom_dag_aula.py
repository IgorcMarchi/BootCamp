import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator # importa os operadores utilizados

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
} 

def push_xcom_with_return():
    return 'my_returned_xcom' # retorna um valor que fica disponível no XCom

def get_pushed_xcom_with_return(**context): # recupera uma informação armazenada no XCom
    print(context['ti'].xcom_pull(task_ids = 't0')) # busca o resultado gerado pela tarefa t0

def push_next_task(**context): # envia para o XCom qual será a próxima tarefa
    context['ti'].xcom_push(key = 'next_task', value = 't3')

def get_next_task(**context): # consulta no XCom qual caminho deve ser seguido
    return context['ti'].xcom_pull(key = 'next_task')

def get_multiple_xcoms(**context): # recupera informações de mais de uma tarefa
    print(context['ti'].xcom_pull(key = None, task_ids = ['t0', 't2']))

with DAG(dag_id = 'xcom_dag_aula', default_args = args, schedule_interval = "@once") as dag: # cria a DAG para uma única execução
    
    t0 = PythonOperator( # cria a primeira tarefa utilizando Python
        task_id = 't0', 
        python_callable = push_xcom_with_return # define a função que será executada
    )

    t1 = PythonOperator( # cria a tarefa que recupera o valor anterior
        task_id = 't1', 
        provide_context = True, 
        python_callable = get_pushed_xcom_with_return # chama a função que consulta o XCom
    )

    t2 = PythonOperator( # cria a tarefa que define o próximo caminho
        task_id = 't2', 
        provide_context = True, 
        python_callable = push_next_task # executa a função que envia o valor ao XCom
    )

    branching = BranchPythonOperator( # cria uma decisão entre diferentes caminhos
        task_id = 'branching', 
        provide_context = True, 
        python_callable = get_next_task, # consulta qual tarefa deve ser executada
    )

    t3 = DummyOperator(task_id = 't3')
        # tarefas usadas como possíveis caminhos da decisão
    t4 = DummyOperator(task_id = 't4')

    t5 = PythonOperator( # cria a tarefa que reúne informações anteriores
        task_id = 't5', 
        trigger_rule = 'one_success', 
        provide_context = True, 
        python_callable = get_multiple_xcoms # recupera diferentes valores do XCom
    )

    t6 = BashOperator( # cria uma tarefa que executa um comando no terminal
        task_id = 't6', # identificação da tarefa
        bash_command = "echo value from xcom: {{ ti.xcom_pull(key = 'next_task') }}" # exibe no terminal o valor armazenado no XCom
    )

    # define o fluxo e a sequência das tarefas
    t0 >> t1
    t1 >> t2 >> branching
    branching >> t3 >> t5 >> t6
    branching >> t4 >> t5 >> t6