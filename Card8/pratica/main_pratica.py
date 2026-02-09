from bs4 import BeautifulSoup
import requests
import time

# Solicita ao usuário uma habilidade que ele não domina
print('Put some skill that you are not familiar with')
unfamiliar_skill = input('> ').lower()
print(f'Filtering out {unfamiliar_skill}')

def find_jobs():
    # Faz a requisição HTTP para o site de vagas do python.org
    html_text = requests.get('https://www.python.org/jobs/').text
    
    # Converte o HTML recebido em um objeto BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')

    # Seleciona todos os elementos <li> que representam vagas de emprego
    jobs = soup.select("ol.list-recent-jobs > li")

    # Percorre cada vaga encontrada
    for index, job in enumerate(jobs):
        # Ignora itens que não possuem título de vaga
        if not job.find("h2"):
            continue

        # Extrai o nome da empresa responsável pela vaga
        company = job.find("span", class_="listing-company-name").text.strip()

        # Extrai a localização da vaga, caso esteja disponível
        location_tag = job.find("span", class_="listing-location")
        location = location_tag.text.strip() if location_tag else "N/A"

        # Extrai a data de publicação da vaga
        date_tag = job.find("time")
        published_date = date_tag.text.strip() if date_tag else "N/A"

        # Obtém todo o texto da vaga e converte para minúsculas
        description = job.text.lower()

        # Verifica se a habilidade informada pelo usuário aparece na descrição da vaga
        if unfamiliar_skill in description:
            continue

        # Cria um arquivo de texto com as informações da vaga
        with open(f'posts/{index}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Job: {index}\n")
            f.write(f"Company: {company}\n")
            f.write(f"Location: {location}\n")
            f.write(f"Published Date: {published_date}\n")

        # Exibe no terminal que o arquivo foi salvo
        print(f'File saved: {index}')

# Ponto de entrada do programa
if __name__ == '__main__':
    # Executa a função de coleta continuamente
    while True:
        find_jobs()
        time_waited = 10
        # Informa o tempo de espera até a próxima execução
        print(f'Waiting {time_waited} minutes...')
        # Aguarda 10 minutos antes de repetir a coleta
        time.sleep(time_waited * 60)
