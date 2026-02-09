# Importa a função reduce
from functools import reduce

# Lista de alunos com nome e nota
alunos = [
    {'nome': 'Ana', 'nota': '7.2'},
    {'nome': 'Breno', 'nota': '8.1'},
    {'nome': 'Claudia', 'nota': '8.7'},
    {'nome': 'Pedro', 'nota': '6.4'},
    {'nome': 'Rafael', 'nota': '6.7'},
]

# Função usada pelo reduce para somar as notas
def somar(a, b): return float(a) + float(b)

# Filtra os alunos aprovados (nota >= 7)
# Em Python 3 usamos list comprehension
alunos_aprovados = [aluno for aluno in alunos if float(aluno['nota']) >= 7]

# Extrai apenas as notas dos alunos aprovados
notas_alunos_aprovados = [aluno['nota'] for aluno in alunos_aprovados]

# Exibe as notas
print(notas_alunos_aprovados)

# Soma todas as notas usando reduce
total = reduce(somar, notas_alunos_aprovados, 0)

# Calcula e exibe a média dos alunos aprovados
print(total / len(alunos_aprovados))
