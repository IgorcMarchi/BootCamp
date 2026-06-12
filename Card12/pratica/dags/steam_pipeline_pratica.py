# Imports 
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import requests


def get_games(): # Função para obter os dados dos jogos mais jogados da Steam
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/" # API da Steam para obter os jogos mais jogados

    response = requests.get(url)
    data = response.json()

    return data["response"]["ranks"][:10]


def save_ranking(ti): # Função para salvar o ranking dos jogos em um arquivo de texto
    games = ti.xcom_pull(task_ids="get_games")

    with open("/opt/airflow/data/ranking.txt", "w", encoding="utf-8") as f: # Abre o arquivo para escrita, criando-o se não existir

        f.write("TOP 10 JOGOS DA STEAM\n\n")

        for game in games: # Itera sobre os jogos e escreve suas informações no arquivo
            f.write(
                f"Rank {game['rank']} | "
                f"AppID {game['appid']} | "
                f"Jogadores {game['peak_in_game']}\n"
            )

    print("Ranking salvo com sucesso!")


def choose_popularity(ti): # Função para escolher o caminho do DAG com base na popularidade do jogo mais jogado
    games = ti.xcom_pull(task_ids="get_games")

    top_game = games[0]

    if top_game["peak_in_game"] > 1000000:
        return "record_game"

    return "normal_game"


with DAG( # Definição do DAG
    dag_id="steam_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    get_games_task = PythonOperator( # Tarefa para obter os dados dos jogos mais jogados
        task_id="get_games",
        python_callable=get_games
    )

    save_ranking_task = PythonOperator( # Tarefa para salvar o ranking dos jogos em um arquivo de texto
        task_id="save_ranking",
        python_callable=save_ranking
    )

    branching = BranchPythonOperator( # Tarefa para escolher o caminho do DAG com base na popularidade do jogo mais jogado
        task_id="choose_popularity",
        python_callable=choose_popularity
    )

    record_game = BashOperator( # Tarefa para registrar a popularidade recorde do jogo mais jogado
        task_id="record_game",
        bash_command='echo "RECORD DE JOGADORES DETECTADO" >> /opt/airflow/logs/steam.log'
    )

    normal_game = BashOperator( # Tarefa para registrar a popularidade normal do jogo mais jogado
        task_id="normal_game",
        bash_command='echo "POPULARIDADE NORMAL" >> /opt/airflow/logs/steam.log'
    )

    finish = EmptyOperator( # tarefa para finalizar a Dag
        task_id="finish",
        trigger_rule="none_failed_min_one_success"
    )

    # Define as sequências das tarefas no DAG

    get_games_task >> save_ranking_task >> branching 

    branching >> [record_game, normal_game]

    [record_game, normal_game] >> finish
