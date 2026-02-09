# Importa a função reduce
from functools import reduce

# Função que retorna outra função para somar um valor às notas
def somar_nota(delta):
    def somar(nota):
        return nota + delta
    return somar

# Lista de notas
notas = [6.4, 7.2, 5.4, 8.4]

# Aplica a função nas notas somando 1.5
notas_finais_1 = list(map(somar_nota(1.5), notas))

# Em Python 3 o resultado do map precisa ser convertido em lista
notas_finais_2 = list(map(somar_nota(1.6), notas))

# Exibe os resultados
print(notas_finais_1)
print(notas_finais_2)

# Nova lista de notas
notas = [6.4, 7.2, 5.4, 8.4]

# Função usada para somar as notas
def somar(a, b):
    return a + b

# Soma todas as notas usando reduce
total = reduce(somar, notas, 0)
print(total)

# Exemplos alternativos sem map 
# for i, nota in enumerate(notas):
#     notas[i] = nota + 1.5

# for i in range(len(notas)):
#     notas[i] = notas[i] + 1.5
