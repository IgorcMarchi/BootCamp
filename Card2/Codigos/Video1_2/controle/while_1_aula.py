
total = 0
nota = 0
qtd = 0

while nota != -1:  # Só sai quando nota for igual a -1
    nota = float(input('Informe o numero ou -1 para sair: '))
    if nota != -1:  # Só soma se receber um numero diferente de -1
        total += nota
        qtd += 1
print(f'A media da turma é {total / qtd}')
