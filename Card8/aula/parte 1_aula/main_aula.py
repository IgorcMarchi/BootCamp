# Importa a biblioteca BeautifulSoup do pacote bs4
from bs4 import BeautifulSoup

with open('home_aula.html', 'r') as html_file:  # Abrir o arquivo HTML em modo de leitura
    content = html_file.read()  # Aplicando o método de leitura do conteúdo do arquivo
    # print(content)  # Imprimir o conteúdo lido do arquivo

    soup = BeautifulSoup(content, 'lxml')  # Criar um objeto BeautifulSoup para analisar o conteúdo HTML usando o parser 'lxml'
    # print(soup.prettify())
    # tags = soup.find('h5') # Encontrar a primeira tag <h5> no HTML
    # tags = soup.find_all('h5')  # Encontrar todas as tags <h5> no HTML

    course_cards = soup.find_all('div', class_='card')  # Encontrar todas as divs com a classe 'card' 
    for course in course_cards: # Interar sobre cada card de curso encontrado
        course_name = course.h5.text  # Extrair o nome do curso da tag <h5> dentro do card
        course_price = course.a.text.split()[-1]  # Extrair o preço do curso da tag <a> dentro do card
        print(f'Curso: {course_name} custa {course_price}')  # Imprimir o nome e o preço do curso
        

