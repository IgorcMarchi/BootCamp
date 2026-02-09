from functools import reduce

print("\n==== TIPOS BASICOS ====")

# Declaracao de variaveis basicas
texto = "corrida"        # string
inteiro = 10            # int
decimal = 2.5          # float
logico = True           # booleano

# Exibe os valores
print(texto, inteiro, decimal, logico)


print("\n==== LISTA ====")

# Criacao de uma lista
lista = [1, 2, 3]

# Adiciona elemento ao final
lista.append(4)

# Insere elemento na posicao 1
lista.insert(1, 99)

# Mostra a lista e seu tamanho
print(lista)
print("Tamanho:", len(lista))


print("\n==== TUPLA ====")

# Tupla e imutavel e permite valores repetidos
tupla = (1, 2, 2, 3,)
print(tupla)


print("\n==== CONJUNTO ====")

# Conjunto nao permite valores duplicados
conjunto = {1, 2, 2, 3, 4}
print(conjunto)


print("\n==== DICIONARIO ====")

# Estrutura de chave e valor
pessoa = {"nome": "Igor", "idade": 20}

# Acesso por chave
print(pessoa["nome"])


print("\n==== OPERADORES ====")

a = 10
b = 3

# Operadores aritmeticos
print(a + b, a - b, a * b, a / b)

# Operadores relacionais
print(a > b, a == b)

# Operadores logicos
print(a > 5 and b < 5)


print("\n==== CONTROLE DE FLUXO ====")

# Estrutura condicional
if a > b:
    print("A maior que B")
else:
    print("B maior que A")


print("\n==== WHILE ====")

# Laco que repete enquanto a condicao for verdadeira
i = 0
while i < 3:
    print(i)
    i += 1


print("\n==== FOR ====")

# Laco com numero definido de repeticoes
for x in range(3):
    print(x)


print("\n==== FUNCOES ====")

# Funcao que soma dois valores


def soma(x, y):
    return x + y


print("Soma:", soma(3, 4))


print("\n==== *args ====")

# Recebe quantidade indefinida de parametros


def soma_varios(*args):
    return sum(args)


print(soma_varios(1, 2, 3, 4))


print("\n==== **kwargs ====")

# Recebe parametros nomeados


def mostrar_dados(**kwargs):
    for k, v in kwargs.items():
        print(k, ":", v)


mostrar_dados(nome="Igor", curso="Python")


print("\n==== MAP / FILTER / REDUCE ====")

numeros = [1, 2, 3, 4]

# Aplica funcao em todos os elementos
dobro = list(map(lambda x: x * 2, numeros))
print("Map:", dobro)

# Filtra elementos pela condicao
maiores = list(filter(lambda x: x >= 3, numeros))
print("Filter:", maiores)

# Reduz lista a um unico valor
soma_total = reduce(lambda x, y: x + y, numeros)
print("Reduce:", soma_total)


print("\n==== POO - ANIMAIS ====")

# Classe base Animal


class Animal:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    # Metodo comum a todos os animais
    def emitir_som(self):
        print("O animal emite um som")

    def comer(self):
        print(f"{self.nome} esta comendo")

    def dormir(self):
        print(f"{self.nome} esta dormindo")


# Classe derivada Cachorro
class Cachorro(Animal):
    def emitir_som(self):
        print(f"{self.nome} diz: Au au")


# Classe derivada Gato
class Gato(Animal):
    def emitir_som(self):
        print(f"{self.nome} diz: Miau")


# Classe derivada Passaro
class Passaro(Animal):
    def emitir_som(self):
        print(f"{self.nome} diz: Piu piu")


# Testes
dog = Cachorro("Marley", 5)
cat = Gato("Cinzento", 3)
bird = Passaro("Loro", 2)

dog.emitir_som()
dog.comer()
dog.dormir()

print()

cat.emitir_som()
cat.comer()
cat.dormir()

print()

bird.emitir_som()
bird.comer()
bird.dormir()
