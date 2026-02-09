for i in range(10):  # de 0 a 9
    print(i)

for i in range(1, 11):  # de 1 a 10
    print(i)

for i in range(1, 100, 7):  # de 1 a 99 aumentando em 7 em 7
    print(i)

for i in range(20, 0, -3):
    print(i)

nums = [2, 4, 6, 8]

for n in nums:
    print(n, end=' ')  # Coloca em uma unica linha com espaços

print('\n')

texto = 'Python é muito massa!'

for i in texto:
    print(i, end=' ')

print('\n')

for n in {1, 2, 3, 4, 4, 4}:  # Não coloca numero repetido
    print(n, end=' ')

print('\n')

produto = {
    'nome': 'caneta',
    'preço': 8.80,
    'desconto': 0.5
}
for atrib in produto:
    print(atrib, '==>', produto[atrib])

print('\n')

for atrib, valor in produto.items():
    print(atrib, '==>', valor)

print('\n')

for valor in produto.values():
    print(valor, end=' ')

print('\n')

for atrib in produto.keys():
    print(atrib, end=' ')
