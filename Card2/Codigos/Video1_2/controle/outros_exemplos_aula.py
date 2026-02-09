pessoas = ['Gui', 'Rebeca']
adjs = ['Sapeca', 'Inteligente']

for p in pessoas:
    for a in adjs:
        print(f'{p} é a {a}!')

for i in [1, 2, 3]:
    pass  # Laço vazio

for i in range(1, 11):
    if i % 2 == 1:
        continue  # ignora a parte do repetição
    print(i)

for i in range(1, 11):
    if i == 5:
        break  # Sai do laço
    print(i)

print('Fim!')
