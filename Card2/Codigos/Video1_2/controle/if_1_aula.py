nota = float(input('Informe a nota do aluno: '))
comportado = True if input('Comportado (s/n) ') == 's' else False

if nota >= 9 and comportado:  # condição de "Se"
    print('Duas palavras: para bens! :P')
    print('Quadro de Honra')
elif nota >= 7:  # condição de "senão se"
    print("Aprovado")
elif nota >= 5.5:
    print('Recuperação')
elif nota >= 3.5:
    print('Recuperação + trabalho')
else:  # condção de "senão"
    print('Reprovado')
print(nota)
