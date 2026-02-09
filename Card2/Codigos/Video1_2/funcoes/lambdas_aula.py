# Importa a função reduce
from functools import reduce

# Lista de alunos
alunos = [
    {'nome': 'Ana', 'nota': '7.2'},
    {'nome': 'Breno', 'nota': '8.1'},
    {'nome': 'Claudia', 'nota': '8.7'},
    {'nome': 'Pedro', 'nota': '6.4'},
    {'nome': 'Rafael', 'nota': '6.7'},
]

# Função que verifica se o aluno foi aprovado
def aluno_aprovado(aluno):
    return float(aluno['nota']) >= 7

# Filtra os alunos aprovados
alunos_aprovados = list(filter(aluno_aprovado, alunos))

# Função que obtém apenas a nota do aluno
def obter_nota(aluno):
    return aluno['nota']

# Função usada pelo reduce para somar as notas
def somar(a, b):
    return float(a) + float(b)

# Aplica filter, map e reduce
alunos_aprovados = list(filter(aluno_aprovado, alunos))
notas_alunos_aprovados = list(map(obter_nota, alunos_aprovados))
total = reduce(somar, notas_alunos_aprovados, 0)

# Calcula e exibe a média dos alunos aprovados
print(total / len(alunos_aprovados))
