# Função com parâmetros padrão
def saudacao(nome='Pessoa', idade=20):
    print(f'Bom dia {nome}!\nVocê nem parece ter {idade} anos!')


# def saudacao():
#     print('Bom dia!')


# Função que realiza soma e multiplicação
def soma_emulti(a, b, x):
    return a + b * x


# Garante que o código abaixo só execute quando o arquivo for o principal
if (__name__ == '__main__'):
    saudacao('Ana', idade=30)
