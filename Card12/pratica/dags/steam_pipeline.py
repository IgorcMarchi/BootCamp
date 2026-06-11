from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import requests


def get_games():
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"

    response = requests.get(url)
    data = response.json()

    return data["response"]["ranks"][:10]


def save_ranking(ti):
    games = ti.xcom_pull(task_ids="get_games")

    with open("/opt/airflow/data/ranking.txt", "w", encoding="utf-8") as f:

        f.write("TOP 10 JOGOS DA STEAM\n\n")

        for game in games:
            f.write(
                f"Rank {game['rank']} | "
                f"AppID {game['appid']} | "
                f"Jogadores {game['peak_in_game']}\n"
            )

    print("Ranking salvo com sucesso!")


def choose_popularity(ti):
    games = ti.xcom_pull(task_ids="get_games")

    top_game = games[0]

    if top_game["peak_in_game"] > 1000000:
        return "record_game"

    return "normal_game"


with DAG(
    dag_id="steam_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    get_games_task = PythonOperator(
        task_id="get_games",
        python_callable=get_games
    )

    save_ranking_task = PythonOperator(
        task_id="save_ranking",
        python_callable=save_ranking
    )

    branching = BranchPythonOperator(
        task_id="choose_popularity",
        python_callable=choose_popularity
    )

    record_game = BashOperator(
        task_id="record_game",
        bash_command='echo "RECORD DE JOGADORES DETECTADO" >> /opt/airflow/logs/steam.log'
    )

    normal_game = BashOperator(
        task_id="normal_game",
        bash_command='echo "POPULARIDADE NORMAL" >> /opt/airflow/logs/steam.log'
    )

    finish = EmptyOperator(
        task_id="finish",
        trigger_rule="none_failed_min_one_success"
    )

    get_games_task >> save_ranking_task >> branching

    branching >> [record_game, normal_game]

    [record_game, normal_game] >> finish
