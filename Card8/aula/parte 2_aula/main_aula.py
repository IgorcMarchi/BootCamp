from bs4 import BeautifulSoup
import requests
import time

# O código não está funcionando porque o site mudou a estrutura do HTML, 
# pois não é possível usar o BeautifulSoup para coletar dados no site que usa JavaScript para carregar o conteúdo.


print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>') # pedir ao usuário para inserir uma habilidade que ele não está familiarizado
print(f'Filtering out {unfamiliar_skill}')

def find_jobs():
    # site para procurar vagas de emprego para Python
    html_text = requests.get('https://www.timesjobs.com/job-search?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation=&refreshed=true', verify=False).text

    soup = BeautifulSoup(html_text, 'lxml')
    # Encontrar as classes de trabalho
    jobs = soup.find('div', class_= 'p-4 md:p-6 bg-white rounded-xl mb-4 shadow-sm relative srp-card')

    for index, job in enumerate(jobs): # repetir sobre as classes de trabalho
        published_date = job.find('span', class_ = 'srp-published').span.text # mostra a data de publicação da vaga
        if 'few' in published_date: # se a data de publicação for pouco então continue
            # Encontrar o nome da empresa
            company_name = job.find('h2', class_ = 'mb-1 text-sm md:text-base font-bold w-[160px] md:w-[430px] whitespace-nowrap overflow-hidden text-ellipsis').text.replace(' ', '')
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '') # mostra as habilidades exigidas para a vaga
            more_info = job.header.h2.a['href'] # mostra o link para mais informações sobre a vaga
            if unfamiliar_skill not in skills: # se a habilidade que o usuário não está familiarizado não estiver nas habilidades exigidas para a vaga então continue
                with open(f'posts/{index}.txt', 'w') as f: # criar um arquivo de texto para cada vaga de emprego
                    f.write(f"Company Name: {company_name.strip()}\n") # escrever o nome da empresa no arquivo de texto
                    f.write(f"Required Skills: {skills.strip()}\n") # escrever as habilidades exigidas para a vaga no arquivo de texto
                    f.write(f"More Info: {more_info}") # escrever o link para mais informações sobre a vaga no arquivo de texto
                print(f'File saved: {index}') # mostrar uma mensagem de que o arquivo foi salvo
if __name__ == '__main__':
    while True:
        find_jobs() # chamar a função para encontrar vagas de emprego
        time_waited = 10
        print(f'Waiting {time_waited} minutes...') # mostrar uma mensagem de espera
        time.sleep(time_waited * 60) # esperar 10 minutos antes de procurar por novas vagas de emprego